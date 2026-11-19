
from src.recomendador import recomendar_escenarios

estudiantes_prueba = [
    "EST001",
    "EST002",
    "EST003",
    "EST004",
    "EST010",
    "EST999"
]

for id_estudiante in estudiantes_prueba:

    resultado = recomendar_escenarios(
        id_estudiante=id_estudiante,
        top_n=3
    )

    print("\n====================================")
    print("ESTUDIANTE:", id_estudiante)
    print("ESTADO:", resultado["estado"])
    print("MENSAJE:", resultado["mensaje"])

    if resultado["estado"] == "ok":

        for posicion, escenario in enumerate(
            resultado["recomendaciones"],
            start=1
        ):

            print(
                f'{posicion}. {escenario["cargo"]} '
                f'- {escenario["puntaje_total"]}%'
            )
