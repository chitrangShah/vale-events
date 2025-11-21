# Vale Events Extractor

Extract local event details from Facebook group images using OCR and LLM.

## Architecture

**Vertical Slice Architecture**
- Each feature is self-contained (endpoint + handler)
- Shared utilities in `shared/` folder

**Processing Pipeline**
1. Download images from Facebook Graph API
2. Extract text using Pytesseract OCR
3. Parse and structure text using Ollama LLM
4. Store events in JSON

## Requirements

- Python 3.12+
- UV package manager
- Tesseract OCR installed on system
- Ollama running locally

## Setup

### 1. Install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Tesseract OCR

```bash
brew install tesseract
```

### 3. Install Ollama
```bash
curl https://ollama.ai/install.sh | sh
```

### 4. Pull Ollama model
```bash
ollama pull llama3.2
```

### 5. Install Python dependencies
```bash
uv sync
```

### 6. Configure environment
Create `.env` file:
```
FACEBOOK_ACCESS_TOKEN=your_token_here
FACEBOOK_GROUP_ID=your_group_id
OLLAMA_MODEL=llama3.2
```

## Run
```bash
uv run python run.py
```

Open http://localhost:8000

## Usage

1. Click "Process New Events" button
2. Wait for processing (downloads → OCR → LLM → storage)
3. View extracted events

## API Endpoints

- `GET /api/events` - Get all events
- `GET /api/events/{id}` - Get specific event
- `POST /api/process` - Trigger processing
- `GET /api/health` - Health check