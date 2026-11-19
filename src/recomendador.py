
from pathlib import Path
import pandas as pd


# ============================================
# 1. CONFIGURACION GENERAL
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_ESTUDIANTES = BASE_DIR / "data" / "estudiantes.csv"
RUTA_ESCENARIOS = BASE_DIR / "data" / "escenarios.csv"

# Pesos del algoritmo: deben sumar 1.0
PESO_COMPETENCIAS = 0.60
PESO_AREA = 0.25
PESO_MODALIDAD = 0.15


# ============================================
# 2. CARGA DE DATOS
# ============================================

def cargar_datos():
    """
    Carga los archivos CSV del proyecto.
    """

    estudiantes = pd.read_csv(
        RUTA_ESTUDIANTES,
        encoding="utf-8"
    )

    escenarios = pd.read_csv(
        RUTA_ESCENARIOS,
        encoding="utf-8"
    )

    return estudiantes, escenarios


# ============================================
# 3. NORMALIZACION DE TEXTO
# ============================================

def normalizar_texto(valor):
    """
    Convierte el texto a minusculas y elimina
    espacios innecesarios.
    """

    if pd.isna(valor):
        return ""

    return str(valor).strip().casefold()


def convertir_competencias(texto):
    """
    Convierte las competencias separadas por |
    en un conjunto de valores normalizados.
    """

    if pd.isna(texto):
        return set()

    return {
        normalizar_texto(competencia)
        for competencia in str(texto).split("|")
        if competencia.strip()
    }


# ============================================
# 4. CALCULO DE COMPATIBILIDAD
# ============================================

def calcular_compatibilidad(estudiante, escenario):
    """
    Calcula la compatibilidad entre un estudiante
    y un escenario de practica profesional.
    """

    competencias_estudiante = convertir_competencias(
        estudiante["competencias"]
    )

    competencias_requeridas = convertir_competencias(
        escenario["competencias_requeridas"]
    )

    # Competencias que coinciden
    coincidencias = (
        competencias_estudiante
        & competencias_requeridas
    )

    # Competencias que le faltan al estudiante
    faltantes = (
        competencias_requeridas
        - competencias_estudiante
    )

    # Puntaje de competencias
    if competencias_requeridas:
        puntaje_competencias = (
            len(coincidencias)
            / len(competencias_requeridas)
        ) * 100
    else:
        puntaje_competencias = 0

    # Puntaje del area de interes
    coincide_area = (
        normalizar_texto(estudiante["area_interes"])
        == normalizar_texto(escenario["area"])
    )

    puntaje_area = 100 if coincide_area else 0

    # Puntaje de modalidad
    coincide_modalidad = (
        normalizar_texto(estudiante["modalidad_preferida"])
        == normalizar_texto(escenario["modalidad"])
    )

    puntaje_modalidad = (
        100 if coincide_modalidad else 0
    )

    # Calculo del puntaje final
    puntaje_total = (
        puntaje_competencias * PESO_COMPETENCIAS
        + puntaje_area * PESO_AREA
        + puntaje_modalidad * PESO_MODALIDAD
    )

    return {
        "puntaje_total": round(puntaje_total, 2),
        "puntaje_competencias": round(
            puntaje_competencias, 2
        ),
        "puntaje_area": puntaje_area,
        "puntaje_modalidad": puntaje_modalidad,
        "competencias_coincidentes": sorted(coincidencias),
        "competencias_faltantes": sorted(faltantes)
    }


# ============================================
# 5. GENERACION DE RECOMENDACIONES
# ============================================

def recomendar_escenarios(id_estudiante, top_n=5):
    """
    Genera un ranking de escenarios disponibles
    para el estudiante seleccionado.

    No realiza asignaciones institucionales.
    """

    estudiantes, escenarios = cargar_datos()

    # Buscar el estudiante
    estudiante_filtrado = estudiantes[
        estudiantes["id_estudiante"].astype(str)
        == str(id_estudiante)
    ]

    if estudiante_filtrado.empty:
        return {
            "estado": "error",
            "mensaje": "El estudiante no existe.",
            "estudiante": None,
            "recomendaciones": []
        }

    estudiante = estudiante_filtrado.iloc[0]

    # Verificar habilitacion simulada
    if normalizar_texto(estudiante["habilitado"]) != "si":
        return {
            "estado": "no_habilitado",
            "mensaje": (
                "El estudiante no esta habilitado "
                "en los datos simulados."
            ),
            "estudiante": estudiante.to_dict(),
            "recomendaciones": []
        }

    # Filtrar escenarios disponibles
    escenarios_disponibles = escenarios[
        (
            escenarios["estado"]
            .astype(str)
            .str.strip()
            .str.casefold()
            == "disponible"
        )
        &
        (
            pd.to_numeric(
                escenarios["cupos"],
                errors="coerce"
            ) > 0
        )
    ]

    if escenarios_disponibles.empty:
        return {
            "estado": "sin_escenarios",
            "mensaje": (
                "No hay escenarios disponibles "
                "con cupos."
            ),
            "estudiante": estudiante.to_dict(),
            "recomendaciones": []
        }

    recomendaciones = []

    # Evaluar cada escenario elegible
    for _, escenario in escenarios_disponibles.iterrows():

        resultado = calcular_compatibilidad(
            estudiante,
            escenario
        )

        recomendacion = {
            "id_escenario": escenario["id_escenario"],
            "empresa": escenario["empresa"],
            "cargo": escenario["cargo"],
            "area": escenario["area"],
            "modalidad": escenario["modalidad"],
            "ciudad": escenario["ciudad"],
            "cupos": int(escenario["cupos"]),
            **resultado
        }

        recomendaciones.append(recomendacion)

    # Ordenar por mayor compatibilidad
    recomendaciones.sort(
        key=lambda item: (
            -item["puntaje_total"],
            -item["puntaje_competencias"],
            item["id_escenario"]
        )
    )

    # Limitar la cantidad de resultados
    if top_n is not None:
        if not isinstance(top_n, int) or top_n < 1:
            raise ValueError(
                "top_n debe ser un entero positivo."
            )

        recomendaciones = recomendaciones[:top_n]

    return {
        "estado": "ok",
        "mensaje": "Recomendaciones generadas correctamente.",
        "estudiante": estudiante.to_dict(),
        "recomendaciones": recomendaciones
    }


# ============================================
# 6. PRUEBA DIRECTA DEL MODULO
# ============================================

if __name__ == "__main__":

    print("\n===================================")
    print("      PRACTIMATCH - ALGORITMO")
    print("===================================")

    resultado = recomendar_escenarios(
        id_estudiante="EST001",
        top_n=5
    )

    print("\nEstado:", resultado["estado"])
    print("Mensaje:", resultado["mensaje"])

    if resultado["estudiante"] is not None:

        print(
            "\nEstudiante:",
            resultado["estudiante"]["nombre"]
        )

    if resultado["estado"] == "ok":

        print("\nTOP 5 ESCENARIOS RECOMENDADOS")

        for posicion, recomendacion in enumerate(
            resultado["recomendaciones"],
            start=1
        ):

            print("\n------------------------------")
            print("Posicion:", posicion)
            print("Empresa:", recomendacion["empresa"])
            print("Cargo:", recomendacion["cargo"])
            print(
                "Compatibilidad:",
                f'{recomendacion["puntaje_total"]}%'
            )
            print(
                "Competencias coincidentes:",
                ", ".join(
                    recomendacion["competencias_coincidentes"]
                ) or "Ninguna"
            )
            print(
                "Competencias faltantes:",
                ", ".join(
                    recomendacion["competencias_faltantes"]
                ) or "Ninguna"
            )
