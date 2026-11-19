# 🎓 PractiMatch — Sistema de Recomendación de Prácticas Profesionales

Prototipo académico de un sistema de recomendación basado en contenido y puntuación ponderada, diseñado para apoyar la identificación de escenarios de práctica profesional compatibles con el perfil, las competencias técnicas y las preferencias de estudiantes de **Ingeniería de Sistemas**.

> **Nota académica:** Todos los registros de estudiantes, empresas y vacantes incluidos en este repositorio son **completamente simulados** con fines exclusivamente educativos. El sistema funciona como herramienta de apoyo a la decisión y no realiza asignaciones institucionales oficiales.

---

## 📋 Información del Proyecto

* **Institución:** Corporación Universitaria del Caribe — CECAR
* **Programa:** Ingeniería de Sistemas
* **Asignatura:** Tecnologías E-Business (2026)
* **Docente:** Guillermo Carlos Hernández Hernández
* **Equipo de desarrollo:** Daniela Díaz Caro y Estefanía Villalba Paternina
* **Tecnologías:** Python, Pandas, Streamlit y archivos CSV

---

## ⚙️ ¿Cómo funciona el algoritmo?

El motor de recomendación (`src/recomendador.py`) evalúa cada estudiante frente a los escenarios disponibles aplicando primero restricciones de elegibilidad (estudiante habilitado y escenario con cupos disponibles) y calculando luego un puntaje de compatibilidad ponderado:

$$P = 0.60C + 0.25A + 0.15M$$

| Criterio | Peso | Descripción |
| :--- | :---: | :--- |
| **Competencias técnicas ($C$)** | **60%** | Proporción de competencias requeridas por la vacante que posee el estudiante. |
| **Área de interés ($A$)** | **25%** | Coincidencia entre el área profesional de interés del estudiante y el área del escenario. |
| **Modalidad preferida ($M$)** | **15%** | Coincidencia entre la modalidad deseada (Presencial, Remoto, Híbrido) y la ofrecida. |

---

## 📁 Estructura del Proyecto

```text
PractiMatch/
├── data/
│   ├── estudiantes.csv          # Perfiles académicos y competencias simuladas (10 registros)
│   └── escenarios.csv           # Ofertas y vacantes simuladas de práctica (12 registros)
├── src/
│   └── recomendador.py          # Lógica de filtrado, cálculo ponderado y ranking
├── app.py                       # Interfaz web interactiva desarrollada en Streamlit
├── verificar_datos.py           # Script de validación de integridad de los archivos CSV
├── probar_recomendador.py       # Script de pruebas por consola para distintos perfiles
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Exclusión de entornos virtuales y archivos temporales
└── README.md                    # Documentación e instrucciones de ejecución
```

---

## 🚀 Guía de Instalación y Ejecución Local

Sigue estos pasos en orden desde tu terminal (PowerShell en Windows, o Terminal en Linux/macOS).

> **💡 Nota sobre el comando de Python:** Dependiendo de cómo esté instalado Python en tu computador, el comando principal puede ser `python`, `py` (común en Windows) o `python3` (común en Linux/macOS). En cada paso encontrarás las tres opciones para que uses la que funcione en tu equipo.

### 1. Clonar el repositorio y entrar a la carpeta

```bash
git clone https://github.com/DannyDC29/PractiMatch.git
cd PractiMatch
```

### 2. Verificar la instalación de Python

Ejecuta **una** de las siguientes opciones hasta ver el número de versión (se recomienda Python 3.10 o superior):

* **Opción A (Estándar):**
  ```bash
  python --version
  ```
* **Opción B (Lanzador de Windows):**
  ```bash
  py --version
  ```
* **Opción C (Linux / macOS):**
  ```bash
  python3 --version
  ```

### 3. Crear y activar el entorno virtual (`.venv`)

Un entorno virtual aísla las librerías del proyecto para evitar conflictos con otros programas de tu computador.

**Paso 3.1 — Crear el entorno virtual** (usa el mismo comando de Python que te funcionó en el paso anterior):
```bash
# Opción A:
python -m venv .venv

# Opción B (Windows):
py -m venv .venv

# Opción C (Linux / macOS):
python3 -m venv .venv
```

**Paso 3.2 — Activar el entorno virtual** según tu sistema operativo:

* **En Windows (PowerShell):**
  *(La primera línea habilita temporalmente la ejecución de scripts en la sesión actual para evitar bloqueos de permisos)*
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  & .\.venv\Scripts\Activate.ps1
  ```
* **En Windows (Símbolo del sistema / CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **En Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

> Sabrás que está activo cuando veas `(.venv)` al inicio de la línea de tu terminal.

### 4. Instalar las dependencias

Con el entorno `(.venv)` activado, instala Streamlit y Pandas:

```bash
# Opción A:
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Opción B (si usas py):
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

# Opción C (si usas python3):
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### 5. (Opcional) Verificar datos y algoritmo por consola

Antes de abrir la interfaz visual, puedes comprobar que los CSV y el motor de recomendación funcionen correctamente:

```bash
python verificar_datos.py
python probar_recomendador.py
```
*(Si usas `py` o `python3`, reemplaza `python` por el comando correspondiente).*

### 6. Ejecutar la aplicación web (Streamlit)

Asegúrate de estar en la carpeta raíz `PractiMatch` con `(.venv)` activo y ejecuta **una** de estas líneas:

```bash
# Opción A:
python -m streamlit run app.py

# Opción B (Windows):
py -m streamlit run app.py

# Opción C (Linux / macOS):
python3 -m streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`.
