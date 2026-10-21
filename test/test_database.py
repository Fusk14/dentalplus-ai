import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from database import inicializar, disponibilidad, reservar, conectar

def test_flujo():
    inicializar()
    horas = disponibilidad(2)
    assert horas, 'No hay horas disponibles para limpieza'
    elegido = horas[0]['horario_id']
    assert not reservar(elegido,2,'Paciente demo',confirmar=False)['ok']
    assert reservar(elegido,2,'Paciente demo',confirmar=True)['ok']
    assert not reservar(elegido,2,'Otro paciente',confirmar=True)['ok']
    assert elegido not in [h['horario_id'] for h in disponibilidad(2)]
    with conectar() as conn:
        conn.execute('DELETE FROM reservas WHERE horario_id=?',(elegido,))

if __name__ == '__main__':
    test_flujo()
    print('Pruebas de reserva y duplicados: OK')
