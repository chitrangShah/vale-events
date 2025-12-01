# Vale Events - Frontend

SvelteKit site displaying events. Deployed on Vercel.

**Live Site:** https://vale-events.vercel.app/

---

## Requirements

- Node.js 20+
- npm

---

## Setup

```bash
cd frontend
npm install
```

---

## Development

```bash
npm run dev
```

Open http://localhost:5173

---

## Deploy

Push to GitHub - Vercel auto-deploys.

```bash
git add static/
git commit -m "Update events"
git push
```

---

## Project Structure

```
frontend/
├── src/
│   ├── routes/
│   │   └── +page.svelte    # Main page
│   └── lib/
│       ├── types.ts        # Event types
│       ├── dateUtils.ts    # Date helpers
│       ├── timeUtils.ts    # Time parsing
│       └── eventUtils.ts   # Event grouping
├── static/
│   ├── api/
│   │   └── events.json     # Event data (from backend)
│   └── images/             # Event images (from backend)
```

---

## Features

- **Event Groups** - Today, Tomorrow, This Week, Next Week, Later
- **Add to Calendar** - Download .ics file
- **Image Viewer** - Click to view full size
- **Responsive** - Mobile friendly

---

## Testing

```bash
npm test
```

---

## Troubleshooting

### Empty Events List

Run backend export:
```bash
cd backend
uv run python scripts/process_and_export.py
```

Then commit frontend changes:
```bash
cd frontend
git add static/
git commit -m "Update events"
git push
```

### Build Fails on Vercel

Check Node version is 22.x in Vercel dashboard:
Project Settings → General → Node.js Version