# Local Source Chat SSE fix (2026-11-10, base v1.15.1)

This extends the upstream image, pinned by tag + digest in the Dockerfile. It
keeps the bundled SSE Route Handler ahead of the general API rewrite, and adds
SSE comment heartbeats every 10 seconds while Source Chat is waiting for Ollama.
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

## Bumping the base image

1. Pull the new tag and copy its `source_chat.py`, `next.config.ts`,
   `.next/routes-manifest.json`, `.next/required-server-files.json` and
   `server.js`; compare the SHA-256 values against `apply_fix.py`.
   (The three frontend build artifacts have been byte-identical since 1.14.0.)
2. Update the expected hash for `source_chat.py` and the `FROM` tag/digest.
3. Diff `lib/locales/en-US/index.ts` against `vi-lang/vi-VN/index.ts` and add
   any new keys (and remove dropped ones) — the frontend build runs `tsc`, and
   `viVN` is declared `satisfies TranslationShape`, so drift fails the build.
4. Diff the new `lib/locales/index.ts` against `vi-lang/locales-index.ts`;
   `check_locales.py` fails the build if a locale is missing.

## Vietnamese locale (vi-VN)

The Dockerfile also bakes in the `vi-VN` translation (see `vi-lang/`):

- COPYs the translated locale and the patched `locales/index.ts` (registers
  `vi-VN`); upstream 1.15 derives the language menu from `lib/locales`, so no
  `LanguageToggle.tsx` patch is needed anymore,
- runs `vi-lang/check_locales.py`, which fails if `locales-index.ts` is missing
  a locale directory present in the base image,
- rebuilds the frontend with `npm ci` + `npm run build`, then restores the
  traced standalone `node_modules`/`server.js` so the image stays lean.

Source of truth for the translation is `../local-vi-lang/`; `vi-lang/`
holds the exact copies used at build time.
