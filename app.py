import html
from pathlib import Path

import pandas as pd
import streamlit as st

from src.recomendador import (
    cargar_datos,
    recomendar_escenarios,
)


# ==================================================
# 1. CONFIGURACION GENERAL
# ==================================================

st.set_page_config(
    page_title="PractiMatch | Recomendador de Practicas",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent


def render_html(bloque_html: str):
    """
    Elimina sangrias y lineas en blanco para evitar que Markdown
    interprete bloques HTML como cuadros de codigo.
    """
    html_limpio = "\n".join(
        linea.strip()
        for linea in bloque_html.splitlines()
        if linea.strip()
    )
    st.markdown(html_limpio, unsafe_allow_html=True)


# ==================================================
# 2. ESTILOS VISUALES
# ==================================================

render_html(
    """
    <style>
    /* Tipografia y fondo general */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    .stApp {
        background-color: #F4F7FB;
        color: #14263D;
    }

    .block-container {
        padding-top: 1.7rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #10243A;
    }

    section[data-testid="stSidebar"] * {
        color: #F2F6FC;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #39516A;
    }

    .sidebar-brand {
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.6px;
        color: #FFFFFF;
        margin-bottom: 0.3rem;
    }

    .sidebar-subtitle {
        color: #C3D3E2;
        font-size: 0.86rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .sidebar-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #9BC8DB;
        margin-bottom: 0.6rem;
    }

    /* Encabezado principal */
    .hero {
        background: linear-gradient(115deg, #10243A 0%, #173D5C 100%);
        border-radius: 18px;
        padding: 30px 34px;
        margin-bottom: 22px;
        color: white;
    }

    .hero-tag {
        color: #A8DAE8;
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.7px;
        line-height: 1.2;
        margin-bottom: 12px;
    }

    .hero-description {
        color: #D3E0EA;
        font-size: 0.96rem;
        line-height: 1.7;
        max-width: 760px;
    }

    /* Tarjetas de indicadores */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E9F0;
        border-radius: 15px;
        padding: 21px;
        min-height: 115px;
        box-shadow: 0 3px 12px rgba(16, 36, 58, 0.035);
    }

    .metric-label {
        color: #65758A;
        font-size: 0.83rem;
        font-weight: 600;
        margin-bottom: 9px;
    }

    .metric-value {
        color: #10243A;
        font-size: 1.9rem;
        font-weight: 800;
        line-height: 1.2;
    }

    /* Titulos de seccion */
    .section-heading {
        color: #14263D;
        font-size: 1.28rem;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 7px;
    }

    .section-description {
        color: #697A8E;
        font-size: 0.89rem;
        margin-bottom: 16px;
    }

    /* Perfil */
    .profile-card {
        background: #FFFFFF;
        border: 1px solid #E2E9F0;
        border-radius: 15px;
        padding: 22px 24px;
        margin-top: 14px;
        margin-bottom: 18px;
    }

    .profile-name {
        font-size: 1.23rem;
        font-weight: 750;
        color: #14263D;
        margin-bottom: 5px;
    }

    .profile-meta {
        color: #64758A;
        font-size: 0.9rem;
        line-height: 1.8;
    }

    /* Recomendaciones */
    .recommendation-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E8F0;
        border-radius: 16px;
        padding: 23px 26px;
        margin-bottom: 17px;
        box-shadow: 0 4px 16px rgba(16, 36, 58, 0.035);
    }

    .recommendation-top {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
    }

    .recommendation-rank {
        font-size: 0.73rem;
        font-weight: 800;
        letter-spacing: 1px;
        color: #287A9A;
        margin-bottom: 8px;
    }

    .recommendation-title {
        font-size: 1.18rem;
        font-weight: 750;
        color: #10243A;
        line-height: 1.4;
        margin-bottom: 5px;
    }

    .recommendation-company {
        font-size: 0.88rem;
        color: #65758A;
    }

    .score {
        color: #176B91;
        font-size: 1.65rem;
        font-weight: 800;
        white-space: nowrap;
    }

    .score-caption {
        font-size: 0.7rem;
        color: #738298;
        text-align: right;
    }

    .progress-track {
        background-color: #EAF0F5;
        height: 9px;
        border-radius: 20px;
        margin-top: 18px;
        margin-bottom: 18px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 20px;
        background: linear-gradient(90deg, #2385A6, #29A18A);
    }

    .card-meta {
        color: #52657A;
        font-size: 0.85rem;
        line-height: 1.9;
        margin-bottom: 13px;
    }

    .skill-title {
        font-size: 0.8rem;
        color: #34495E;
        font-weight: 750;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .skill-chip {
        display: inline-block;
        padding: 5px 10px;
        margin: 0 6px 6px 0;
        border-radius: 7px;
        background-color: #E6F6F0;
        color: #176B54;
        font-size: 0.76rem;
        font-weight: 600;
    }

    .skill-chip.missing {
        background-color: #FFF3E5;
        color: #936018;
    }

    .explanation {
        background-color: #F3F7FB;
        border-radius: 10px;
        padding: 13px 15px;
        margin-top: 15px;
        color: #45596F;
        font-size: 0.84rem;
        line-height: 1.7;
    }

    .footer {
        text-align: center;
        color: #7A899A;
        font-size: 0.78rem;
        padding: 28px 10px 10px;
    }

    /* Botones de Streamlit */
    div.stButton > button[kind="primary"] {
        background-color: #176B91;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #105675;
        color: #FFFFFF;
    }

    /* Selectores */
    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }

    /* Adaptacion a pantallas pequenas */
    @media (max-width: 650px) {
        .hero {
            padding: 22px;
        }

        .hero-title {
            font-size: 1.5rem;
        }

        .recommendation-card {
            padding: 18px;
        }

        .recommendation-title {
            font-size: 1rem;
        }

        .score {
            font-size: 1.3rem;
        }
    }
    </style>
    """
)


# ==================================================
# 3. FUNCIONES VISUALES
# ==================================================

def texto_seguro(valor):
    """
    Escapa caracteres especiales antes de insertar
    valores de los CSV dentro del HTML.
    """
    return html.escape(str(valor), quote=True)


def mostrar_indicador(titulo, valor):
    render_html(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                {texto_seguro(titulo)}
            </div>
            <div class="metric-value">
                {texto_seguro(valor)}
            </div>
        </div>
        """
    )


def mostrar_etiquetas(competencias, faltantes=False):
    if not competencias:
        return (
            '<span style="color:#748398;font-size:0.82rem;">'
            'Ninguna'
            '</span>'
        )

    clase = "skill-chip missing" if faltantes else "skill-chip"

    return "".join(
        f'<span class="{clase}">{texto_seguro(item)}</span>'
        for item in competencias
    )


def explicar_recomendacion(recomendacion):
    """
    Construye una explicacion sencilla usando
    los resultados reales del algoritmo.
    """
    partes = []

    puntaje_competencias = recomendacion["puntaje_competencias"]

    if puntaje_competencias == 100:
        partes.append("cumple todas las competencias requeridas")
    elif puntaje_competencias > 0:
        partes.append("cumple parcialmente las competencias requeridas")
    else:
        partes.append("no presenta coincidencias en las competencias requeridas")

    if recomendacion["puntaje_area"] == 100:
        partes.append("el area coincide con su interes profesional")
    else:
        partes.append("el area no coincide con su interes principal")

    if recomendacion["puntaje_modalidad"] == 100:
        partes.append("la modalidad coincide con su preferencia")
    else:
        partes.append("la modalidad es diferente a su preferencia")

    return (
        "Esta puntuacion se obtiene porque el estudiante "
        + "; ".join(partes)
        + "."
    )


def mostrar_recomendacion(recomendacion, posicion):
    puntaje = float(recomendacion["puntaje_total"])
    ancho = max(0, min(100, puntaje))

    competencias = mostrar_etiquetas(
        recomendacion["competencias_coincidentes"]
    )

    faltantes = mostrar_etiquetas(
        recomendacion["competencias_faltantes"],
        faltantes=True,
    )

    explicacion = explicar_recomendacion(recomendacion)

    render_html(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-top">
                <div>
                    <div class="recommendation-rank">
                        RECOMENDACION #{posicion}
                    </div>
                    <div class="recommendation-title">
                        {texto_seguro(recomendacion["cargo"])}
                    </div>
                    <div class="recommendation-company">
                        {texto_seguro(recomendacion["empresa"])}
                    </div>
                </div>
                <div>
                    <div class="score">
                        {puntaje:.1f}%
                    </div>
                    <div class="score-caption">
                        Compatibilidad
                    </div>
                </div>
            </div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{ancho:.2f}%"></div>
            </div>
            <div class="card-meta">
                <strong>Area:</strong>
                {texto_seguro(recomendacion["area"])}
                &nbsp; | &nbsp;
                <strong>Modalidad:</strong>
                {texto_seguro(recomendacion["modalidad"])}
                <br>
                <strong>Ciudad:</strong>
                {texto_seguro(recomendacion["ciudad"])}
                &nbsp; | &nbsp;
                <strong>Cupos:</strong>
                {texto_seguro(recomendacion["cupos"])}
            </div>
            <div class="skill-title">
                Competencias coincidentes
            </div>
            <div>{competencias}</div>
            <div class="skill-title">
                Competencias por fortalecer
            </div>
            <div>{faltantes}</div>
            <div class="explanation">
                <strong>¿Por que se recomienda?</strong>
                <br>
                {texto_seguro(explicacion)}
            </div>
        </div>
        """
    )


# ==================================================
# 4. CARGA DE INFORMACION
# ==================================================

try:
    estudiantes, escenarios = cargar_datos()

except (FileNotFoundError, pd.errors.ParserError, UnicodeError) as error:
    st.error(
        "No fue posible cargar los archivos CSV. "
        "Verifica la carpeta data."
    )
    st.code(str(error))
    st.stop()


# ==================================================
# 5. BARRA LATERAL
# ==================================================

with st.sidebar:
    render_html(
        """
        <div class="sidebar-brand">
            🎓 PractiMatch
        </div>
        <div class="sidebar-subtitle">
            Sistema inteligente de apoyo
            a la recomendacion de escenarios
            de practicas profesionales.
        </div>
        """
    )

    st.divider()

    render_html('<div class="sidebar-label">Navegacion</div>')

    seccion = st.radio(
        "Selecciona una seccion",
        [
            "Panel de recomendaciones",
            "Base de datos",
            "Acerca del proyecto",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    render_html('<div class="sidebar-label">Informacion</div>')

    st.caption("Institucion: CECAR")
    st.caption("Programa: Ingenieria de Sistemas")
    st.caption("Proyecto academico - 2026")
    st.caption("Datos completamente simulados")

    st.divider()

    st.caption(
        "Desarrollado por Daniela Diaz Caro "
        "y Estefania Villalba Paternina."
    )


# ==================================================
# 6. ENCABEZADO
# ==================================================

render_html(
    """
    <div class="hero">
        <div class="hero-tag">
            PROTOTIPO ACADEMICO · TECNOLOGIAS E-BUSINESS
        </div>
        <div class="hero-title">
            Recomendaciones inteligentes
            para practicas profesionales
        </div>
        <div class="hero-description">
            Analiza competencias, intereses y preferencias
            de estudiantes de Ingenieria de Sistemas
            para identificar escenarios de practica
            potencialmente compatibles.
        </div>
    </div>
    """
)


# ==================================================
# 7. INDICADORES GENERALES
# ==================================================

total_estudiantes = len(estudiantes)
total_escenarios = len(escenarios)

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

total_disponibles = len(escenarios_disponibles)

col1, col2, col3, col4 = st.columns(4)

with col1:
    mostrar_indicador("Estudiantes registrados", total_estudiantes)

with col2:
    mostrar_indicador("Escenarios registrados", total_escenarios)

with col3:
    mostrar_indicador("Escenarios disponibles", total_disponibles)

with col4:
    mostrar_indicador("Criterios de evaluacion", 3)


# ==================================================
# 8. PANEL DE RECOMENDACIONES
# ==================================================

if seccion == "Panel de recomendaciones":
    render_html('<div class="section-heading">Perfil del estudiante</div>')
    render_html(
        '<div class="section-description">'
        'Selecciona un estudiante y configura '
        'la cantidad de resultados que deseas consultar.'
        '</div>'
    )

    opciones_estudiantes = {
        str(fila["id_estudiante"]): (
            f'{fila["nombre"]} ({fila["id_estudiante"]})'
        )
        for _, fila in estudiantes.iterrows()
    }

    if not opciones_estudiantes:
        st.warning("No existen estudiantes registrados.")
        st.stop()

    columna_estudiante, columna_top = st.columns([3, 1])

    with columna_estudiante:
        id_seleccionado = st.selectbox(
            "Seleccionar estudiante",
            options=list(opciones_estudiantes.keys()),
            format_func=lambda identificador: (
                opciones_estudiantes[identificador]
            ),
        )

    with columna_top:
        cantidad = st.selectbox(
            "Resultados a mostrar",
            options=[3, 5, 10],
            index=1,
        )

    estudiante_seleccionado = estudiantes[
        estudiantes["id_estudiante"].astype(str)
        == str(id_seleccionado)
    ].iloc[0]

    estado_habilitacion = str(
        estudiante_seleccionado["habilitado"]
    ).strip().casefold()

    estado_texto = (
        "Habilitado"
        if estado_habilitacion == "si"
        else "No habilitado"
    )

    render_html(
        f"""
        <div class="profile-card">
            <div class="profile-name">
                {texto_seguro(estudiante_seleccionado["nombre"])}
            </div>
            <div class="profile-meta">
                <strong>Programa:</strong>
                {texto_seguro(estudiante_seleccionado["programa"])}
                &nbsp; | &nbsp;
                <strong>Semestre:</strong>
                {texto_seguro(estudiante_seleccionado["semestre"])}
                <br>
                <strong>Area de interes:</strong>
                {texto_seguro(estudiante_seleccionado["area_interes"])}
                &nbsp; | &nbsp;
                <strong>Modalidad preferida:</strong>
                {texto_seguro(estudiante_seleccionado["modalidad_preferida"])}
                <br>
                <strong>Estado:</strong>
                {texto_seguro(estado_texto)}
            </div>
            <div class="skill-title">
                Competencias del estudiante
            </div>
            <div>
                {mostrar_etiquetas(
                    [
                        competencia.strip()
                        for competencia in str(
                            estudiante_seleccionado["competencias"]
                        ).split("|")
                        if competencia.strip()
                    ]
                )}
            </div>
        </div>
        """
    )

    parametros = (
        str(id_seleccionado),
        int(cantidad),
    )

    if (
        st.session_state.get("parametros_recomendacion")
        != parametros
    ):
        st.session_state["parametros_recomendacion"] = None
        st.session_state["resultado_recomendacion"] = None

    if st.button(
        "🔎 Generar recomendaciones",
        type="primary",
        use_container_width=True,
    ):
        try:
            resultado = recomendar_escenarios(
                id_estudiante=id_seleccionado,
                top_n=cantidad,
            )

            st.session_state["resultado_recomendacion"] = resultado
            st.session_state["parametros_recomendacion"] = parametros

        except (
            FileNotFoundError,
            pd.errors.ParserError,
            UnicodeError,
            KeyError,
            ValueError,
        ) as error:
            st.session_state["resultado_recomendacion"] = None
            st.error("Ocurrio un problema al generar las recomendaciones.")
            st.code(str(error))

    resultado_guardado = st.session_state.get("resultado_recomendacion")

    if (
        resultado_guardado is not None
        and st.session_state.get("parametros_recomendacion") == parametros
    ):
        if resultado_guardado["estado"] == "ok":
            recomendaciones = resultado_guardado["recomendaciones"]

            render_html(
                '<div class="section-heading">Escenarios recomendados</div>'
            )
            render_html(
                '<div class="section-description">'
                'Resultados ordenados de mayor a menor '
                'compatibilidad calculada.'
                '</div>'
            )

            st.success(
                f"Se generaron {len(recomendaciones)} "
                "recomendaciones correctamente."
            )

            for posicion, recomendacion in enumerate(
                recomendaciones,
                start=1,
            ):
                mostrar_recomendacion(recomendacion, posicion)

            st.info(
                "Los porcentajes son puntuaciones "
                "de compatibilidad del prototipo. "
                "No representan probabilidades de "
                "contratacion ni asignaciones oficiales."
            )

        elif resultado_guardado["estado"] == "no_habilitado":
            st.warning(
                "El estudiante seleccionado no esta "
                "habilitado en los datos simulados. "
                "No se generaron recomendaciones."
            )

        elif resultado_guardado["estado"] == "sin_escenarios":
            st.warning(
                "No existen escenarios disponibles "
                "con cupos en este momento."
            )

        else:
            st.error(resultado_guardado["mensaje"])


# ==================================================
# 9. PANEL DE BASE DE DATOS
# ==================================================

elif seccion == "Base de datos":
    render_html(
        '<div class="section-heading">Explorador de datos simulados</div>'
    )
    render_html(
        '<div class="section-description">'
        'Consulta los registros utilizados '
        'para el funcionamiento del prototipo.'
        '</div>'
    )

    pestana1, pestana2 = st.tabs(
        ["Estudiantes", "Escenarios de practica"]
    )

    with pestana1:
        st.subheader("Estudiantes registrados")
        st.dataframe(
            estudiantes,
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Informacion ficticia creada para pruebas academicas."
        )

    with pestana2:
        st.subheader("Escenarios registrados")
        st.dataframe(
            escenarios,
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Organizaciones y vacantes simuladas. "
            "No corresponden a ofertas reales."
        )


# ==================================================
# 10. INFORMACION DEL PROYECTO
# ==================================================

elif seccion == "Acerca del proyecto":
    render_html('<div class="section-heading">Acerca de PractiMatch</div>')

    st.write(
        "PractiMatch es un prototipo academico "
        "de sistema de recomendacion orientado "
        "a apoyar la identificacion de escenarios "
        "de practica profesional para estudiantes "
        "de Ingenieria de Sistemas."
    )

    st.subheader("¿Como funciona?")
    st.write("1. Se selecciona un estudiante registrado.")
    st.write(
        "2. El sistema verifica su habilitacion "
        "simulada y la disponibilidad de escenarios."
    )
    st.write(
        "3. Calcula la compatibilidad mediante "
        "competencias, area de interes y modalidad."
    )
    st.write(
        "4. Ordena los escenarios de mayor a menor "
        "puntuacion y explica los resultados."
    )

    st.subheader("Criterios y pesos")

    tabla_pesos = pd.DataFrame(
        {
            "Criterio": [
                "Competencias tecnicas",
                "Area de interes",
                "Modalidad preferida",
            ],
            "Peso": [
                "60%",
                "25%",
                "15%",
            ],
        }
    )

    st.dataframe(
        tabla_pesos,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Alcance")
    st.info(
        "Este sistema utiliza datos simulados "
        "y funciona como herramienta de apoyo "
        "a la decision. No reemplaza la evaluacion "
        "del coordinador ni realiza asignaciones "
        "institucionales."
    )

    st.subheader("Tecnologias")
    st.write("Python, Pandas, Streamlit y archivos CSV.")

    st.subheader("Equipo de desarrollo")
    st.write("Daniela Diaz Caro y Estefania Villalba Paternina.")


# ==================================================
# 11. PIE DE PAGINA
# ==================================================

render_html(
    """
    <div class="footer">
        PractiMatch © 2026 · Prototipo academico
        <br>
        Corporacion Universitaria del Caribe - CECAR
        <br>
        Datos simulados · Uso exclusivamente educativo
    </div>
    """
)