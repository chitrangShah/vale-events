# Vale Events - Backend

Extracts event data from flyer images using Ollama Vision (llama3.2-vision).

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- [Ollama](https://ollama.ai/) with llama3.2-vision model

---

## Setup

### 1. Install Dependencies

```bash
cd backend
uv sync
```

### 2. Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Start Ollama & Pull Model

```bash
ollama serve          # Start server (keep running)
ollama pull llama3.2-vision   # In another terminal
```

---

## Usage

```bash
# Add images
cp ~/Downloads/event-flyer.jpg data/images/

# Process
uv run python scripts/process_and_export.py
```

**What happens:**
1. AI vision model reads each image
2. Extracts: name, date, time, location, price, etc.
3. Saves JSON to `data/events/`
4. Exports to `../frontend/static/`

---

## Project Structure

```
backend/
├── data/
│   ├── images/          # Add flyer images here
│   └── events/          # Generated JSON files
├── scripts/
│   └── process_and_export.py
└── src/
    ├── features/
    │   └── process_events/
    │       └── handler.py
    └── shared/
        └── clients/
            └── llm_client.py    # Ollama Vision client
```

---

## Troubleshooting

### "Ollama not responding"

Start the server:
```bash
ollama serve
```

### "Model not found"

Pull the vision model:
```bash
ollama pull llama3.2-vision
```

### "ModuleNotFoundError"

Run from the backend directory:
```bash
cd backend
uv run python scripts/process_and_export.py
```

---

## Testing

```bash
uv run pytest
```