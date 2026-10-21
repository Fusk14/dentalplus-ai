from pathlib import Path
import csv
import sqlite3
from datetime import date, datetime

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
DB = ROOT / 'data' / 'database' / 'dentalplus.db'

SCHEMA = '''
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS especialidades (especialidad_id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS profesionales (profesional_id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, especialidad_id INTEGER NOT NULL REFERENCES especialidades(especialidad_id));
CREATE TABLE IF NOT EXISTS tratamientos (tratamiento_id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE, especialidad_id INTEGER NOT NULL REFERENCES especialidades(especialidad_id), precio_clp INTEGER NOT NULL CHECK(precio_clp >= 0), duracion_min INTEGER NOT NULL CHECK(duracion_min > 0));
CREATE TABLE IF NOT EXISTS horarios (horario_id INTEGER PRIMARY KEY, fecha TEXT NOT NULL, hora TEXT NOT NULL, profesional_id INTEGER NOT NULL REFERENCES profesionales(profesional_id), UNIQUE(fecha,hora,profesional_id));
CREATE TABLE IF NOT EXISTS reservas (reserva_id INTEGER PRIMARY KEY AUTOINCREMENT, horario_id INTEGER NOT NULL UNIQUE REFERENCES horarios(horario_id), tratamiento_id INTEGER NOT NULL REFERENCES tratamientos(tratamiento_id), paciente_alias TEXT NOT NULL, estado TEXT NOT NULL DEFAULT 'confirmada' CHECK(estado = 'confirmada'), creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
'''

def conectar():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB, timeout=10)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    return conn

def cargar_csv(nombre):
    with (RAW / f'{nombre}.csv').open(encoding='utf-8-sig', newline='') as archivo:
        return list(csv.DictReader(archivo))

def inicializar():
    with conectar() as conn:
        conn.executescript(SCHEMA)
        for tabla, columnas in (
            ('especialidades',('especialidad_id','nombre')),
            ('profesionales',('profesional_id','nombre','especialidad_id')),
            ('tratamientos',('tratamiento_id','nombre','especialidad_id','precio_clp','duracion_min')),
            ('horarios',('horario_id','fecha','hora','profesional_id')),
        ):
            filas = cargar_csv(tabla)
            if tabla == 'horarios':
                for fila in filas:
                    date.fromisoformat(fila['fecha'])
                    datetime.strptime(fila['hora'], '%H:%M')
            cols = ','.join(columnas)
            placeholders = ','.join('?' for _ in columnas)
            conn.executemany(f'INSERT OR IGNORE INTO {tabla} ({cols}) VALUES ({placeholders})',
                             [[fila[col] for col in columnas] for fila in filas])
    return DB

def disponibilidad(tratamiento_id, fecha=None):
    sql = '''SELECT h.horario_id, h.fecha, h.hora, p.nombre AS profesional, t.nombre AS tratamiento
             FROM horarios h JOIN profesionales p ON p.profesional_id=h.profesional_id
             JOIN tratamientos t ON t.especialidad_id=p.especialidad_id
             LEFT JOIN reservas r ON r.horario_id=h.horario_id
             WHERE t.tratamiento_id=? AND r.reserva_id IS NULL AND h.fecha>=?'''
    args = [tratamiento_id, date.today().isoformat()]
    if fecha:
        date.fromisoformat(fecha)
        sql += ' AND h.fecha=?'
        args.append(fecha)
    sql += ' ORDER BY h.fecha,h.hora LIMIT 20'
    with conectar() as conn:
        return [dict(f) for f in conn.execute(sql,args)]

def reservar(horario_id, tratamiento_id, paciente_alias, confirmar=False):
    if not confirmar:
        return {'ok':False,'mensaje':'Se requiere confirmación explícita del paciente.'}
    if not paciente_alias.strip():
        return {'ok':False,'mensaje':'Falta el alias del paciente.'}
    with conectar() as conn:
        conn.execute('BEGIN IMMEDIATE')
        valido = conn.execute('''SELECT 1 FROM horarios h JOIN profesionales p ON p.profesional_id=h.profesional_id
              JOIN tratamientos t ON t.especialidad_id=p.especialidad_id
              WHERE h.horario_id=? AND t.tratamiento_id=? AND h.fecha>=?''',
              (horario_id,tratamiento_id,date.today().isoformat())).fetchone()
        if not valido:
            return {'ok':False,'mensaje':'Horario inexistente, pasado o incompatible con el tratamiento.'}
        try:
            cursor = conn.execute('INSERT INTO reservas(horario_id,tratamiento_id,paciente_alias) VALUES(?,?,?)',
                                  (horario_id,tratamiento_id,paciente_alias.strip()))
        except sqlite3.IntegrityError:
            return {'ok':False,'mensaje':'La hora ya fue reservada.'}
        return {'ok':True,'reserva_id':cursor.lastrowid,'mensaje':'Reserva registrada.'}

if __name__ == '__main__':
    print('Base inicializada:', inicializar())
    print('Horas de limpieza:', disponibilidad(2)[:3])
