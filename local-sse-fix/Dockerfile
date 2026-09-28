FROM lfnovo/open_notebook@sha256:80d1b5ad4aead7266c37c9fa9cad33d5075f6549eeda5d4cbf8668a58366d824
COPY _sse_keepalive.py /app/api/routers/_sse_keepalive.py
COPY apply_fix.py /tmp/apply_sse_fix.py
RUN /app/.venv/bin/python /tmp/apply_sse_fix.py
LABEL local.open-notebook.fix="source-chat-sse-20260921"
