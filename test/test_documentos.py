"""Verificación básica de coherencia entre documentos simulados y CSV."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'data' / 'documentos'
RAW = ROOT / 'data' / 'raw'


def probar():
    archivos = sorted(DOCS.glob('*.md'))
    assert len(archivos) == 4, 'Deben existir 4 documentos Markdown.'
    for archivo in archivos:
        contenido = archivo.read_text(encoding='utf-8')
        assert 'SIMULAD' in contenido, f'Falta aviso de simulación: {archivo.name}'
    if RAW.exists() and (RAW / 'tratamientos.csv').exists():
        with (RAW / 'tratamientos.csv').open(encoding='utf-8-sig', newline='') as f:
            tratamientos = list(csv.DictReader(f))
        servicios = (DOCS / '01_servicios.md').read_text(encoding='utf-8')
        for tratamiento in tratamientos:
            assert tratamiento['nombre'] in servicios, f"Falta servicio {tratamiento['nombre']}"
            assert f"${int(tratamiento['precio_clp']):,}".replace(',', '.') in servicios, 'Precio inconsistente'
    print('OK: documentos presentes y consistentes con los CSV disponibles.')

if __name__ == '__main__':
    probar()
