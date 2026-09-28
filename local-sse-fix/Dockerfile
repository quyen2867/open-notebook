FROM lfnovo/open_notebook@sha256:80d1b5ad4aead7266c37c9fa9cad33d5075f6549eeda5d4cbf8668a58366d824
COPY _sse_keepalive.py /app/api/routers/_sse_keepalive.py
COPY apply_fix.py /tmp/apply_sse_fix.py
RUN /app/.venv/bin/python /tmp/apply_sse_fix.py
LABEL local.open-notebook.fix="source-chat-sse-20260921"

# Vietnamese locale: COPY translated files, insert the `vietnamese` display-name
# key into every locale, then rebuild the frontend. Runtime deps are restored
# to the traced standalone set (mirrors upstream) to keep the image lean.
COPY vi-lang/vi-VN/index.ts /app/frontend/src/lib/locales/vi-VN/index.ts
COPY vi-lang/locales-index.ts /app/frontend/src/lib/locales/index.ts
COPY vi-lang/LanguageToggle.tsx /app/frontend/src/components/common/LanguageToggle.tsx
COPY vi-lang/add_vietnamese_key.py /tmp/apply_vi_lang.py
RUN python3 /tmp/apply_vi_lang.py
RUN cd /app/frontend \
 && npm ci --no-audit --no-fund \
 && npm run build \
 && rm -rf node_modules \
 && cp -r .next/standalone/node_modules ./node_modules \
 && cp .next/standalone/server.js ./server.js \
 && rm -rf /root/.npm /tmp/apply_vi_lang.py
LABEL local.open-notebook.i18n="vi-VN-20250929"
