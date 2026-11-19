
from pathlib import Path
import pandas as pd

# Ruta de la carpeta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Ubicacion de los archivos CSV
RUTA_ESTUDIANTES = BASE_DIR / "data" / "estudiantes.csv"
RUTA_ESCENARIOS = BASE_DIR / "data" / "escenarios.csv"

# Leer los datos
estudiantes = pd.read_csv(RUTA_ESTUDIANTES, encoding="utf-8")
escenarios = pd.read_csv(RUTA_ESCENARIOS, encoding="utf-8")

# Verificar estructura
columnas_estudiantes = {
    "id_estudiante", "nombre", "programa", "semestre",
    "competencias", "area_interes", "modalidad_preferida",
    "ciudad", "habilitado"
}

columnas_escenarios = {
    "id_escenario", "empresa", "cargo", "area",
    "competencias_requeridas", "modalidad",
    "ciudad", "cupos", "estado"
}

assert set(estudiantes.columns) == columnas_estudiantes, (
    "Las columnas de estudiantes.csv no coinciden."
)

assert set(escenarios.columns) == columnas_escenarios, (
    "Las columnas de escenarios.csv no coinciden."
)

assert len(estudiantes) == 10, (
    "Se esperaban 10 estudiantes."
)

assert len(escenarios) == 12, (
    "Se esperaban 12 escenarios."
)

assert not estudiantes.isnull().any().any(), (
    "Hay datos vacios en estudiantes.csv."
)

assert not escenarios.isnull().any().any(), (
    "Hay datos vacios en escenarios.csv."
)

assert estudiantes["id_estudiante"].is_unique, (
    "Hay identificadores de estudiantes repetidos."
)

assert escenarios["id_escenario"].is_unique, (
    "Hay identificadores de escenarios repetidos."
)

# Mostrar resultados
print("\n========================================")
print("      VERIFICACION DE PRACTIMATCH")
print("========================================")

print(f"\nEstudiantes cargados: {len(estudiantes)}")
print(f"Escenarios cargados: {len(escenarios)}")

print("\nPrimeros estudiantes:")
print(estudiantes[["id_estudiante", "nombre", "area_interes"]].head())

print("\nPrimeros escenarios:")
print(escenarios[["id_escenario", "empresa", "area"]].head())

print("\nEstudiantes habilitados:")
print(estudiantes["habilitado"].value_counts())

print("\nEstados de escenarios:")
print(escenarios["estado"].value_counts())

print("\nVERIFICACION COMPLETADA CORRECTAMENTE")
