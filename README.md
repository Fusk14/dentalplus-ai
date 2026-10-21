# DentalPlus — Asistente inteligente para gestión de clínica dental

## 1. Descripción del proyecto

DentalPlus es un prototipo académico de asistente inteligente para una clínica dental ficticia, desarrollado en Python.

El proyecto busca facilitar la consulta de información sobre servicios, profesionales y políticas de atención, además de gestionar una agenda simulada de reservas dentales.

La solución combina una base de datos SQLite, recuperación semántica mediante RAG (Retrieval-Augmented Generation), FAISS y un modelo de lenguaje Gemini.

El objetivo final es integrar estos componentes mediante LangGraph para construir un agente conversacional capaz de consultar información, utilizar herramientas, gestionar reservas y mantener el contexto de una conversación.

**Estado actual:** base de datos, recuperación semántica y generación de respuestas con RAG implementadas. La integración del agente con LangGraph se encuentra pendiente.

## 2. Objetivos

- Implementar una base de datos con información simulada de una clínica dental.
- Consultar servicios, profesionales, horarios y reservas.
- Recuperar información institucional mediante búsqueda semántica.
- Generar respuestas utilizando Gemini y documentos recuperados.
- Integrar herramientas y memoria conversacional mediante LangGraph.
- Evaluar el funcionamiento del prototipo mediante pruebas.

## 3. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje principal del proyecto |
| SQLite | Almacenamiento de información y reservas |
| Pandas | Manipulación y exploración de datos |
| LangChain | Integración de modelos, documentos y recuperación |
| Sentence Transformers | Generación de embeddings |
| FAISS | Búsqueda por similitud semántica |
| Gemini API | Generación de respuestas |
| LangGraph | Orquestación del agente (pendiente) |
| Jupyter Notebook | Desarrollo y validación experimental |
| Git y GitHub | Control de versiones y publicación del proyecto |

## 4. Estructura del proyecto

```text
dentalplus-ai/
│
├── data/
│   ├── raw/
│   │   ├── especialidades.csv
│   │   ├── profesionales.csv
│   │   ├── tratamientos.csv
│   │   └── horarios.csv
│   │
│   ├── documentos/
│   │   ├── 01_servicios.md
│   │   ├── 02_profesionales.md
│   │   ├── 03_politicas_reserva.md
│   │   └── 04_preguntas_frecuentes.md
│   │
│   └── database/
│       └── dentalplus.db
│
├── notebooks/
│   ├── 01_exploracion_y_validacion_datos.ipynb
│   └── 02_recuperacion_rag.ipynb
│
├── src/
│   ├── database.py
│   ├── rag.py
│   ├── llm.py
│   └── asistente_rag.py
│
├── tests/
│   ├── test_database.py
│   └── test_documentos.py
│
├── generar_datos.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

**Nota:** la estructura representa la organización propuesta para el avance actual. El archivo `.env` y la carpeta `.venv` existen localmente, pero no deben publicarse. El archivo `dentalplus.db` se genera localmente y también se excluye de Git.

## 5. Datos utilizados

El proyecto utiliza exclusivamente información ficticia para simular el funcionamiento de una clínica dental pequeña.

El conjunto de datos contiene:

- 3 especialidades.
- 3 profesionales.
- 3 tratamientos.
- 10 días hábiles futuros con 3 bloques de atención por profesional, equivalentes a 90 horarios simulados.

Los servicios considerados son:

| Servicio | Profesional | Precio referencial |
|---|---|---|
| Evaluación dental | Ana Martínez | $20.000 CLP |
| Limpieza dental | Carlos Rojas | $35.000 CLP |
| Evaluación de endodoncia | Sofía Pérez | $30.000 CLP |

Los nombres, precios y horarios son ficticios y se utilizan únicamente con fines académicos.

## 6. Instalación y configuración

### Requisitos previos

- Python instalado.
- Visual Studio Code o un editor compatible.
- Acceso a Google AI Studio para obtener una API Key de Gemini.

### Instalación

Clonar el repositorio:

```powershell
git clone URL_DEL_REPOSITORIO
cd dentalplus-ai
```

Crear el entorno virtual:

```powershell
python -m venv .venv
```

Activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

### Configuración de Gemini

Crear un archivo `.env` en la raíz del proyecto, tomando como referencia `.env.example`.

```dotenv
GOOGLE_API_KEY=TU_CLAVE_PERSONAL
```

La clave real debe mantenerse privada. El archivo `.env` está excluido del repositorio mediante `.gitignore`.

### Generación de datos

Desde la raíz del proyecto:

```powershell
python generar_datos.py
python src/database.py
```

Los archivos CSV se generan en `data/raw/` y la base de datos SQLite se almacena en `data/database/dentalplus.db`.

## 7. Funcionalidades implementadas

### 7.1 Base de datos y agenda

El módulo `src/database.py` permite trabajar con información estructurada de la clínica.

Incluye operaciones de consulta y registro de reservas simuladas.

El registro de reservas requiere confirmación explícita y rechaza intentos de reservar horarios ya ocupados.

### 7.2 Documentación institucional

La carpeta `data/documentos/` contiene información sobre servicios, profesionales, políticas de reserva y preguntas frecuentes.

Estos documentos constituyen la base de conocimiento utilizada por el sistema RAG.

### 7.3 Recuperación semántica

El módulo `src/rag.py` permite:

- Cargar documentos Markdown.
- Dividirlos en fragmentos.
- Generar embeddings mediante un modelo multilingüe.
- Construir un índice vectorial FAISS.
- Recuperar fragmentos relevantes mediante similitud semántica.

### 7.4 Integración con Gemini

El módulo `src/llm.py` configura el modelo de lenguaje mediante LangChain y utiliza una API Key almacenada en variables de entorno.

### 7.5 Asistente RAG

El módulo `src/asistente_rag.py` combina la recuperación de documentos con Gemini para generar respuestas basadas en información institucional.

El asistente tiene instrucciones para evitar inventar información, entregar diagnósticos clínicos o confirmar reservas no registradas.

Esta funcionalidad se encuentra implementada y en proceso de evaluación.

## 8. Pruebas y validación

El proyecto incluye pruebas para comprobar el funcionamiento de la base de datos y la consistencia de los documentos institucionales.

Desde la raíz del proyecto:

```powershell
python tests/test_database.py
python tests/test_documentos.py
```

También se utilizan notebooks para validar la recuperación semántica y las respuestas del asistente.

Debido a los límites de solicitudes de la API gratuita de Gemini, se consideran pruebas locales y modelos simulados para reducir el consumo durante el desarrollo.

## 9. Organización de notebooks

| Notebook | Propósito |
|---|---|
| `01_exploracion_y_validacion_datos.ipynb` | Preparación del entorno, exploración de datos y validación de SQLite |
| `02_recuperacion_rag.ipynb` | Pruebas de embeddings, FAISS, Gemini y respuestas RAG |
| `03_agente_langgraph.ipynb` | Integración y evaluación del agente (pendiente de creación) |

La lógica principal se mantiene en módulos Python dentro de `src/`. Los notebooks se utilizan como entornos de experimentación y validación.

## 10. Próximas etapas

- Implementar herramientas para consultar disponibilidad y gestionar reservas.
- Construir el flujo de orquestación mediante LangGraph.
- Incorporar memoria conversacional.
- Integrar confirmaciones explícitas antes de registrar reservas.
- Desarrollar pruebas del agente completo.
- Elaborar el diagrama de arquitectura y los entregables académicos.

## 11. Limitaciones

DentalPlus es un prototipo académico y no representa un sistema clínico real.

No utiliza datos personales reales ni cuenta con autenticación de pacientes.

El campo `paciente_alias` corresponde a un identificador ficticio utilizado para las demostraciones.

Actualmente no incluye cancelaciones automáticas, duración variable de tratamientos ni sincronización con una agenda clínica real.

Las respuestas generadas por Gemini dependen de la calidad de los documentos recuperados y de la disponibilidad y cuota de la API.

La gestión de reservas mediante conversación y la memoria del agente todavía no están implementadas.

Para regenerar una demostración desde cero, se puede eliminar la base de datos local y ejecutar nuevamente los scripts de generación. No debe eliminarse una base que contenga reservas que se deseen conservar.

## 12. Contexto académico

Proyecto desarrollado con fines educativos para la asignatura de Inteligencia Artificial, utilizando una clínica ficticia como escenario de aplicación.

Toda la información presentada es simulada y no debe utilizarse para decisiones médicas o administrativas reales.
