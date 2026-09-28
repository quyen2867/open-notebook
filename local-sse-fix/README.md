# Local Source Chat SSE fix (2026-09-21)

This extends the existing v1-dev image, pinned by digest in Dockerfile. It keeps
the bundled SSE Route Handler ahead of the general API rewrite, and adds SSE
comment heartbeats every 10 seconds while Source Chat is waiting for Ollama.
The handler already exists in the upstream build, so no JavaScript bundles are
rebuilt: the source configuration, compiled routing manifest and standalone
configuration are updated together, with exact input SHA-256 checks.

`docker-compose.override.yml` selects the local image automatically. All
existing environment variables, ports and data mounts are inherited unchanged
from docker-compose.yml. No database schema or model settings are changed.

Rebuild from this directory's parent:

```sh
docker compose build open_notebook
docker compose up -d --no-deps open_notebook
```

The local image is pinned and `docker compose pull` skips it. To return to the
upstream image (also the starting point for a future upstream update):
```sh
mv docker-compose.override.yml docker-compose.override.yml.disabled
docker compose up -d --no-deps open_notebook
```

The original upstream image is retained. Do not run `docker compose down -v`.
The local patch does not add token-by-token output: the UI waits for the full
model answer, with the SSE connection kept open during that wait.

## Vietnamese locale (vi-VN)

The Dockerfile also bakes in the `vi-VN` translation (see `vi-lang/`):

- COPYs the translated locale, the patched `locales/index.ts` (registers
  `vi-VN`) and the patched `LanguageToggle.tsx` (adds the dropdown item),
- runs `vi-lang/add_vietnamese_key.py` to insert the `vietnamese`
  display-name key into every locale (idempotent),
- rebuilds the frontend with `npm ci` + `npm run build`, then restores the
  traced standalone `node_modules`/`server.js` so the image stays lean.

Source of truth for the translation is `../local-vi-lang/`; `vi-lang/`
holds the exact copies used at build time.
