# OCRE AI — Frontend

React SPA for the OCRE AI project. Provides a UI for browsing and searching the Roman coin catalog, managing a personal collection, uploading coin images for AI identification, and chatting with an AI numismatics expert.

## Tech stack

- **React 19**, **React Router 7** (SPA mode, `ssr: false`)
- **MUI v9** (Material UI + Emotion) for UI components
- **TailwindCSS v4** (Vite plugin) for layout and spacing utilities
- **Zustand** for global client state
- **React Hook Form** + **Zod** for form validation
- **TypeScript** (strict), **ESLint**, **Prettier**
- **pnpm** package manager

## Project structure

```
app/
  routes.ts            # Route config (React Router v7 API)
  root.tsx             # Layout shell, global CSS, error boundary
  app.css              # Global styles
  theme.ts             # MUI theme
  routes/              # Route-level components
    login.tsx
    sign-up.tsx
    forget-password.tsx
    reset-password.tsx
    private-layout.tsx # Authenticated layout wrapper
    catalog.tsx        # Coin list / search page
    catalog-detail.tsx # Single coin detail page
    profile.tsx        # User profile page
  features/            # Feature-scoped components
    auth/
    catalog/
    chat/
    profile/
  components/          # Shared components
    layout/
    ColorSchemeToggle.tsx
  services/            # API client layer
    api.ts             # Axios instance, auth header injection
    auth.service.ts
    catalog.service.ts
    chat.service.ts
    user.service.ts
  store/               # Zustand stores
  lib/                 # Utility helpers
```

## Routes

| Path                     | Access      | Description                   |
|--------------------------|-------------|-------------------------------|
| `/`                      | Public      | Login page                    |
| `/sign-up`               | Public      | Registration                  |
| `/forget-password`       | Public      | Request password reset email  |
| `/reset-password/:token` | Public      | Set new password via token    |
| `/catalog`               | Authenticated | Coin catalog with search/filters |
| `/catalog/:id`           | Authenticated | Coin detail page              |
| `/profile`               | Authenticated | User profile and collection   |

## Local development

### Prerequisites

- Node.js 20+
- pnpm
- Backend running at `http://localhost:8000` (see `apps/backend/README.md`)

### Setup

```bash
cp .env.example .env   # if needed — VITE_API_BASE_URL defaults to http://localhost:8000
pnpm install
pnpm dev               # http://localhost:5173
```

### Commands

```bash
pnpm dev          # Start dev server with HMR (http://localhost:5173)
pnpm build        # Production build → build/client + build/server
pnpm start        # Serve the production build
pnpm typecheck    # Run react-router typegen + tsc
pnpm lint         # ESLint
pnpm lint:fix     # ESLint with auto-fix
pnpm format       # Prettier (write)
pnpm format:check # Prettier (check only)
```

## Configuration

The only runtime variable is the backend base URL:

| Variable            | Default                  | Description              |
|---------------------|--------------------------|--------------------------|
| `VITE_API_BASE_URL` | `http://localhost:8000`  | Backend API base URL     |

In Docker, this is set to `/api` at build time so nginx can proxy requests (see `docker-compose.yml`).

## Deployment

The app is served as static files behind **nginx**, which also reverse-proxies `/api/*` to the backend. The `Dockerfile` performs a multi-stage build:

1. **Build stage** — installs dependencies and runs `pnpm build`
2. **Serve stage** — copies `build/client/` into an nginx image using `nginx.conf`

The nginx config serves the SPA shell for all non-API routes (`try_files $uri $uri/ /index.html`).

To build and run the container standalone:

```bash
docker build --build-arg VITE_API_BASE_URL=/api -t ocre-ai-frontend .
docker run -p 80:80 ocre-ai-frontend
```

For the full stack, use Docker Compose from the repository root — see the [root README](../../README.md).
