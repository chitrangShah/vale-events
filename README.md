# Vale Events

Extract event details from flyer images using AI vision and display them on a simple web UI.

**Live Site:** https://vale-events.vercel.app/

---

## How It Works

```
1. Add flyer images     →  2. Run script  →  3. Push to GitHub  →  4. Live on Vercel
   backend/data/images/     (AI extracts      (auto-deploys)
                             event data)
```

---

## Quick Start

### Prerequisites

- Python 3.12+ with [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.ai/) with `llama3.2-vision` model
- Node.js 20+

### Setup

```bash
git clone https://github.com/chitrangShah/vale-events.git
cd vale-events

# Backend
cd backend
uv sync
ollama pull llama3.2-vision

# Frontend
cd ../frontend
npm install
```

### Process Events

```bash
# 1. Add images
cp ~/Downloads/*.jpg backend/data/images/

# 2. Process (extracts event data using AI vision)
cd backend
uv run python scripts/process_and_export.py

# 3. Deploy
cd ../frontend
git add static/
git commit -m "Add new events"
git push
```

---

## Features

- **AI Vision** - Extracts event details directly from images (no OCR needed)
- **Add to Calendar** - Download .ics files for any event
- **Responsive UI** - Works on desktop and mobile
- **Free** - Local AI processing + free Vercel hosting

---

## Project Structure

```
vale-events/
├── backend/           # Python processing (local)
│   ├── data/images/   # Add flyer images here
│   └── scripts/       # Processing script
│
├── frontend/          # SvelteKit UI (Vercel)
│   └── static/        # Exported events + images
```

See [backend/README.md](./backend/README.md) and [frontend/README.md](./frontend/README.md) for details.

---

## Future Enhancements

~~- Automated Facebook group image fetching~~ (Facebook deprecated groups api to fetch posts information)
- User upload of events images/flyers
- Background processing with GitHub Actions
- Event search and filtering
- Calendar view
- Email notifications for new events
- Event Tracking

## License

MIT