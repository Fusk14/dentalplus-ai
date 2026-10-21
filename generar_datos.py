from pathlib import Path
import csv
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'data' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)

def guardar(nombre, campos, filas):
    with (RAW / nombre).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(campos)
        w.writerows(filas)

especialidades = [(1,'Odontología general'),(2,'Higiene dental'),(3,'Endodoncia')]
profesionales = [(1,'Ana Martínez',1),(2,'Carlos Rojas',2),(3,'Sofía Pérez',3)]
tratamientos = [(1,'Evaluación dental',1,20000,30),(2,'Limpieza dental',2,35000,45),(3,'Evaluación de endodoncia',3,30000,30)]

guardar('especialidades.csv',['especialidad_id','nombre'],especialidades)
guardar('profesionales.csv',['profesional_id','nombre','especialidad_id'],profesionales)
guardar('tratamientos.csv',['tratamiento_id','nombre','especialidad_id','precio_clp','duracion_min'],tratamientos)

# Horarios futuros relativos a la fecha de ejecución: 10 días hábiles, 3 profesionales, 3 bloques.
horarios = []
dia = date.today() + timedelta(days=1)
while len({fila[1] for fila in horarios}) < 10:
    if dia.weekday() < 5:
        for profesional_id in (1,2,3):
            for hora in ('09:00','11:00','15:00'):
                horarios.append((len(horarios)+1,dia.isoformat(),hora,profesional_id))
    dia += timedelta(days=1)
guardar('horarios.csv',['horario_id','fecha','hora','profesional_id'],horarios)
print(f'Se generaron 4 CSV en {RAW} con {len(horarios)} horarios.')
