# Vale Events

Event extraction and management system using OCR (PaddleOCR) and LLM (Ollama) to automatically process event flyer images into structured data.

[![Backend CI](![](https://img.shields.io/badge/Backend%20--blue?style=for-the-badge&logo=python))](https://github.com/chitrangShah/vale_events/actions/workflows/backend-ci.yml)
[![Frontend CI](![](https://img.shields.io/badge/Frontend--b983d8?style=for-the-badge&logo=svelte))](https://github.com/chitrangShah/vale_events/actions/workflows/frontend-ci.yml)
[![Vercel Deployment](https://img.shields.io/badge/vercel-deployed-success)](https://vale-events.vercel.app/)

**Live Site:** https://vale-events.vercel.app/

---

## Architecture
```
Backend (Local Processing)          Frontend (Vercel)
├── PaddleOCR (Text extraction)    ├── SvelteKit
├── Ollama LLM (Data parsing)      ├── Static JSON API
└── Export to frontend/static/     └── Responsive UI
```

**Workflow:**
1. Add event flyer images to `backend/data/images/`
2. Run processing script (OCR + LLM)
3. Script exports JSON and images to `frontend/static/`
4. Commit and push to GitHub
5. Vercel auto-deploys updated events

---

## Quick Start

### Prerequisites

**Backend:**
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- [Ollama](https://ollama.ai/) installed and running

**Frontend:**
- Node.js 20+
- npm

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/vale_events.git
cd vale_events

# Backend setup
cd backend
uv sync
ollama pull llama3.2

# Frontend setup
cd ../frontend
npm install
```

---

## Usage

### Process New Events
```bash
# 1. Add images to backend/data/images/
cp ~/Downloads/*.jpg backend/data/images/

# 2. Process images (runs OCR + LLM locally)
cd backend
uv run python scripts/process_and_export.py

# 3. Deploy to Vercel
cd ../frontend
git add static/
git commit -m "Add new events"
git push
```

Vercel will automatically deploy in ~30 seconds.

---

## Project Structure
```
vale_events/
├── backend/              # Python processing (local only)
│   ├── src/             # Source code
│   ├── data/            # Images and processed events
│   └── scripts/         # Processing scripts
│
├── frontend/            # SvelteKit UI (deployed to Vercel)
│   ├── src/            # Source code
│   └── static/         # Static assets (JSON + images)
│
└── .github/            # CI/CD workflows
    └── workflows/
```

---

## Documentation

- [Backend Setup & Usage](./backend/README.md)
- [Frontend Setup & Usage](./frontend/README.md)

---

## Technology Stack

**Backend:**
- Python 3.12
- PaddleOCR 3.3.2 (text extraction)
- Ollama + llama3.2 (LLM parsing)
- FastAPI (optional local API)

**Frontend:**
- SvelteKit 2.0
- TypeScript
- Vercel (hosting)

---

## Features

- ✅ Automated OCR text extraction from event flyers
- ✅ LLM-powered structured data extraction
- ✅ Beautiful responsive UI
- ✅ "Add to Calendar" (.ics download)
- ✅ Full-size image modal view
- ✅ Free hosting (Vercel)
- ✅ 100% free processing (local OCR + LLM)

---

## Future Enhancements

- Automated Facebook group image fetching
- Background processing with GitHub Actions
- Event search and filtering
- Calendar view
- Email notifications for new events
- Multi-language support
- Event Tracking

---

## License

MIT

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## Support

For issues or questions, please [open an issue](https://github.com/chitrangShah/vale_events/issues).