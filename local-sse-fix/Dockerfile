FROM lfnovo/open_notebook:1.15.1@sha256:e4e18f12653df5bf48674b7b187c4252be52238b4d706330fd30d9b177b95812
COPY _sse_keepalive.py /app/api/routers/_sse_keepalive.py
COPY apply_fix.py /tmp/apply_sse_fix.py
RUN /app/.venv/bin/python /tmp/apply_sse_fix.py
LABEL local.open-notebook.fix="source-chat-sse-20261110"

# Vietnamese locale: COPY the translated files, then rebuild the frontend.
# Upstream 1.15 derives the language menu from lib/locales, so registering
# vi-VN in locales/index.ts is enough — no LanguageToggle patch needed.
# Runtime deps are restored to the traced standalone set (mirrors upstream)
# to keep the image lean.
COPY vi-lang/vi-VN/index.ts /app/frontend/src/lib/locales/vi-VN/index.ts
COPY vi-lang/locales-index.ts /app/frontend/src/lib/locales/index.ts
COPY vi-lang/check_locales.py /tmp/check_locales.py
RUN python3 /tmp/check_locales.py
RUN cd /app/frontend \
 && npm ci --no-audit --no-fund \
 && npm run build \
 && rm -rf node_modules \
 && cp -r .next/standalone/node_modules ./node_modules \
 && cp .next/standalone/server.js ./server.js \
 && rm -rf /root/.npm /tmp/check_locales.py
LABEL local.open-notebook.i18n="vi-VN-20261110"
