# IT Ticket Classifier & Translator

AI-powered IT helpdesk ticket triage and translation using local LLMs via Ollama.

It bridges the gap between non-technical user descriptions and professional IT diagnostics — no cloud APIs, no data leaving your network.

Clasificación y traducción de tickets de soporte TI mediante modelos LLM ejecutados localmente con Ollama. Actúa como puente entre descripciones no técnicas de usuarios y diagnósticos profesionales de TI, sin APIs externas y sin que los datos salgan de tu red.

---

## Language / Idioma

* English
* Español

---

# English

## What it does

Paste any chaotic or non-technical IT support ticket and get an instant structured technical classification:

* Category — Hardware, Software, Network, Security, Access/IAM, Email, Database, Infrastructure.
* Priority — Critical, High, Medium or Low (calculated based on impact).
* Team — Recommended support team.
* Summary (The Translator) — Converts non-technical user descriptions into a concise professional IT diagnostic.
* Confidence — Model certainty score.
* Reasoning — Step-by-step explanation behind the classification.

## Technology Stack

* Backend: FastAPI + Python
* AI Inference: Ollama (local)
* Models: Qwen2.5, DeepSeek-R1 or any Ollama-compatible model
* Frontend: Vanilla HTML, CSS and JavaScript

## Requirements

* Python 3.10+
* Ollama running locally
* At least one downloaded model

Example:

```bash
ollama pull qwen2.5
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/davidgj98/ticket-classifier.git
cd ticket-classifier
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download a model

```bash
ollama pull qwen2.5
```

### 4. Start the application

```bash
uvicorn main:app --reload --port 8000
```

### 5. Open the web interface

```text
http://localhost:8000
```

## API Endpoints

| Method | Path      | Description                     |
| ------ | --------- | ------------------------------- |
| GET    | /         | Web interface                   |
| POST   | /classify | Classify and translate a ticket |
| GET    | /models   | List available Ollama models    |
| GET    | /health   | Health check                    |

## Example Request

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
        "text":"The internet globe icon on my taskbar has a red cross and the floor box is flashing red"
      }'
```

## Example Response

```json
{
  "category": "Network",
  "priority": "High",
  "team": "Network Team",
  "summary": "Local WAN link failure / Router hardware alert status (Red LED flashing)",
  "confidence": "High",
  "reasoning": "User describes a red cross on the network icon and flashing red LEDs on the router, indicating a physical or link-layer connectivity issue."
}
```

---

# Español

## ¿Qué hace?

Pega cualquier incidencia descrita por un usuario sin conocimientos técnicos y obtén una clasificación profesional y estructurada al instante:

* Categoría — Hardware, Software, Redes, Seguridad, Accesos/IAM, Correo, Base de Datos, Infraestructura.
* Prioridad — Crítica, Alta, Media o Baja.
* Equipo — Equipo técnico recomendado.
* Resumen (El Traductor) — Convierte explicaciones vagas en un diagnóstico profesional de TI.
* Confianza — Nivel de certeza del modelo.
* Razonamiento — Explicación paso a paso de la clasificación.

## Stack Tecnológico

* Backend: FastAPI + Python
* Inferencia IA: Ollama (local)
* Modelos: Qwen2.5, DeepSeek-R1 o cualquier modelo compatible con Ollama
* Frontend: HTML, CSS y JavaScript nativo

## Requisitos

* Python 3.10+
* Ollama ejecutándose localmente
* Al menos un modelo descargado

Ejemplo:

```bash
ollama pull qwen2.5
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/davidgj98/ticket-classifier.git
cd ticket-classifier
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Descargar un modelo

```bash
ollama pull qwen2.5
```

### 4. Iniciar la aplicación

```bash
uvicorn main:app --reload --port 8000
```

### 5. Abrir la interfaz web

```text
http://localhost:8000
```

## Endpoints de la API

| Método | Ruta      | Descripción                   |
| ------ | --------- | ----------------------------- |
| GET    | /         | Interfaz web                  |
| POST   | /classify | Clasificar y traducir ticket  |
| GET    | /models   | Modelos disponibles en Ollama |
| GET    | /health   | Estado del servicio           |

## Ejemplo de Petición

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
        "text":"El icono de Internet tiene una cruz roja y el router tiene luces rojas parpadeando"
      }'
```

## Ejemplo de Respuesta

```json
{
  "category": "Network",
  "priority": "High",
  "team": "Network Team",
  "summary": "Pérdida de conectividad WAN / Fallo de enlace en router local",
  "confidence": "High",
  "reasoning": "El usuario describe pérdida de conectividad junto con alertas físicas en el router, lo que apunta a un problema de red o hardware."
}
```

---

# Project Structure / Estructura del Proyecto

```text
ticket-classifier/
├── main.py
├── requirements.txt
├── static/
│   └── index.html
└── README.md
```

## Future Roadmap / Próximas Mejoras

* [ ] Batch classification via CSV upload.
* [ ] Export results to CSV or JSON.
* [ ] Jira and ServiceNow integration.
* [ ] Local ticket history using SQLite.
* [ ] Slack and Microsoft Teams integration.
* [ ] Multi-language classification support.
* [ ] Confidence score visualization.
* [ ] Support for custom classification categories.

## License / Licencia

MIT

