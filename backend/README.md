# Vale Events - Backend

Local processing system for extracting event data from flyer images using OCR and LLM.

---

## Requirements

- **Python:** 3.12 or higher
- **Package Manager:** [uv](https://docs.astral.sh/uv/)
- **LLM:** [Ollama](https://ollama.ai/) with llama3.2 model

---

## Installation

### 1. Install Python Dependencies
```bash
cd backend
uv sync
```

This installs:
- PaddleOCR (text extraction)
- Ollama Python client
- FastAPI (optional API server)

### 2. Install Ollama

**macOS:**
```bash
brew install ollama
ollama serve
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

**Windows:**
Download from https://ollama.ai/download

### 3. Pull LLM Model
```bash
ollama pull llama3.2
```

---

## Usage

### Process Event Images
```bash
# 1. Add images to data/images/
cp ~/Downloads/event-flyer.jpg data/images/

# 2. Run processing script
uv run python scripts/process_and_export.py
```

**What it does:**
1. Extracts text from images using PaddleOCR
2. Parses structured data using Ollama LLM
3. Saves JSON files to `data/events/`
4. Exports JSON and images to `../frontend/static/`

**Output:**
```
Processing Events
============================================================
  Processing: event-flyer.jpg
    Event: Christmas Boutique
    Saved: event-flyer.json
  ✓ Complete

Exporting to Frontend
============================================================
  Exported 5 events to frontend/static/api/events.json
  Copied 5 images to frontend/static/images/

Next steps:
  1. cd frontend
  2. git add static/
  3. git commit -m 'Add new events'
  4. git push
```

---

## Directory Structure
```
backend/
├── src/
│   ├── features/
│   │   ├── process_events/      # Event processing logic
│   │   │   ├── handler.py       # Main handler
│   │   │   └── routes.py        # API routes (optional)
│   │   └── get_events/          # Event retrieval
│   └── shared/
│       ├── clients/
│       │   ├── ocr_client.py    # PaddleOCR wrapper
│       │   └── llm_client.py    # Ollama wrapper
│       └── models/
│           └── event.py         # Event data model
│
├── data/
│   ├── images/                  # Source images (add here)
│   └── events/                  # Processed JSON files
│
├── scripts/
│   └── process_and_export.py   # Main processing script
│
├── pyproject.toml              # Python dependencies
└── uv.lock                     # Dependency lock file
```

---

## Configuration

### Environment Variables

Create `.env` file (optional):
```bash
# OCR Settings
OCR_CONFIDENCE_THRESHOLD=0.3

# LLM Settings
LLM_MODEL=llama3.2
LLM_TEMPERATURE=0.0
```

---

## Optional: Run Local API Server
```bash
uv run python src/main.py
```

**Endpoints:**
- `GET /api/events` - List all events
- `GET /api/events/{id}` - Get specific event
- `POST /api/events/process` - Process images
- `GET /health` - Health check

API docs: http://localhost:8000/docs

---

## Troubleshooting

### Ollama Not Running

**Error:** `Connection refused to localhost:11434`

**Fix:**
```bash
ollama serve
```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'src'`

**Fix:** Make sure you're in the `backend` directory:
```bash
cd backend
uv run python scripts/process_and_export.py
```

### OCR Quality Issues

- Use high-resolution images (at least 1000px width)
- Ensure good contrast between text and background
- Avoid heavily compressed JPEGs

---

## Testing
```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check .
```

---

## Development

### Add New Features

1. Create feature directory in `src/features/`
2. Implement handler in `handler.py`
3. Add routes in `routes.py` (if needed)
4. Register routes in `src/main.py`

### Modify OCR/LLM Logic

- **OCR:** Edit `src/shared/clients/ocr_client.py`
- **LLM:** Edit `src/shared/clients/llm_client.py`

---

## Dependencies

- **paddleocr** - OCR text extraction
- **paddlepaddle** - PaddleOCR backend
- **ollama** - LLM API client
- **fastapi** - API framework (optional)
- **pydantic** - Data validation

Full list: See `pyproject.toml`