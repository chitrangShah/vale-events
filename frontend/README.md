# Vale Events - Frontend

Static SvelteKit website displaying processed events. Deployed on Vercel.

**Live Site:** https://vale-events.vercel.app/

---

## Requirements

- **Node.js:** 20 or higher
- **Package Manager:** npm

---

## Installation
```bash
cd frontend
npm install
```

---

## Development

### Run Local Dev Server
```bash
npm run dev
```

Open http://localhost:5173

**Features:**
- Hot module reloading
- TypeScript checking
- Instant updates

---

## Build

### Production Build
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

---

## Deployment

### Automatic (Recommended)

1. Push to GitHub
2. Vercel automatically deploys
3. Live in ~30 seconds

### Manual
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

---

## Project Structure
```
frontend/
├── src/
│   ├── routes/
│   │   └── +page.svelte        # Main events page
│   └── app.html                # HTML template
│
├── static/
│   ├── api/
│   │   └── events.json         # Event data (exported from backend)
│   └── images/                 # Event images (exported from backend)
│
├── svelte.config.js            # SvelteKit config
├── vite.config.ts              # Vite config
├── package.json                # Dependencies
└── tsconfig.json               # TypeScript config
```

---

## Features

### Event Display
- Responsive grid layout
- Event cards with images
- Date, time, location display
- Organization info
- Price badges

### Image Viewer
- Click image to view full size
- Modal overlay
- Close with ESC or click outside

### Add to Calendar
- Download .ics file
- Compatible with:
  - Google Calendar
  - Apple Calendar
  - Outlook
  - Any iCal-compatible app

### Mobile Friendly
- Responsive breakpoints
- Touch-optimized
- Single column on mobile

---

## Configuration

### Update API URL (if needed)

Edit `src/routes/+page.svelte`:
```typescript
// For local testing with backend API
const response = await fetch('http://localhost:8000/api/events');

// For production (static JSON)
const response = await fetch('/api/events.json');
```

---

## Styling

### Theme Colors

Current gradient: Purple/Blue

To change, edit `+page.svelte`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Responsive Breakpoints
```css
@media (max-width: 768px)  /* Tablet */
@media (max-width: 480px)  /* Mobile */
```

---

## Adding Static Files

### New Event Data

Backend script automatically exports to:
- `static/api/events.json` (consolidated data)
- `static/images/` (event images)

### Other Static Assets

Add to `static/` directory:
- Favicon: `static/favicon.png`
- Icons: `static/icons/`
- Fonts: `static/fonts/`

---

## Troubleshooting

### Build Fails on Vercel

**Check:**
1. All files committed to git
2. `package.json` has build script
3. `svelte.config.js` exists
4. Node version >= 20

**View build logs:**
- Vercel Dashboard → Deployments → Click deployment → View logs

### Empty Events List

**Possible causes:**
1. `static/api/events.json` missing
2. JSON file not committed to git
3. Invalid JSON format

**Fix:**
```bash
# Run backend export script
cd backend
uv run python scripts/process_and_export.py

# Commit frontend changes
cd ../frontend
git add static/
git commit -m "Update events"
git push
```

### Images Not Loading

**Check:**
1. Images in `static/images/`
2. Image paths in JSON are correct
3. Files committed to git

---

## Dependencies

- **@sveltejs/kit** - Framework
- **@sveltejs/adapter-vercel** - Vercel adapter
- **svelte** - UI library
- **vite** - Build tool
- **typescript** - Type checking

Full list: See `package.json`

---

## Vercel Configuration

### Build Settings

- **Framework:** SvelteKit
- **Build Command:** `npm run build`
- **Output Directory:** `build`
- **Install Command:** `npm install`
- **Node Version:** 20.x

### Environment Variables

None required (static site).

---