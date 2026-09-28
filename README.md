# 📓 Open Notebook
ghi chú, chat với tài liệu, tạo podcast — kèm **giao diện tiếng Việt** và fix SSE cho Source Chat.

## ✨ Có gì trong repo này

| Thành phần | Mô tả |
|---|---|
| `docker-compose.yml` | 2 services: `surrealdb` (DB) + `open_notebook` (Web UI `:8502`, API `:5055`) |
| `local-sse-fix/` | Patch giữ kết nối SSE khi Source Chat chờ Ollama (không streaming token-by-token) |
| `local-vi-lang/` | Patch locale `vi-VN` + thêm **Tiếng Việt** vào menu Language |
| `.env.example` | Mẫu biến môi trường (key mã hoá, user/pass DB) |

## 🚀 Chạy thử

```bash
cp .env.example .env   # điền OPEN_NOTEBOOK_ENCRYPTION_KEY
docker compose up -d
```

Mở trình duyệt:

- Web UI: http://localhost:8502/
- REST API: http://localhost:5055/
- SurrealDB (debug): http://127.0.0.1:8000

> Lần đầu mở Language ở sidebar sẽ chưa có tiếng Việt nếu dùng image gốc —
> xem mục Việt hoá bên dưới.

## 🇻🇳 Việt hoá giao diện

Bản build đang chạy đã gồm locale `vi-VN` (963 keys, test parity 34/34 pass).
Nguồn patch nằm ở `local-vi-lang/`:

- `vi-VN/index.ts` — toàn bộ bản dịch
- `index.ts` — đăng ký `vi-VN` vào `resources`/`languages`
- `LanguageToggle.tsx` — thêm item **Tiếng Việt** vào dropdown
- `en-US-index.ts` — bản gốc đối chiếu
- `add_vi_patch.py` — script chèn key `vietnamese` + item dropdown vào image gốc

Áp patch vào container đang chạy (cho image chưa có sẵn):

```bash
docker cp local-vi-lang/vi-VN/index.ts <container>:/app/frontend/src/lib/locales/vi-VN/index.ts
docker cp local-vi-lang/index.ts <container>:/app/frontend/src/lib/locales/index.ts
docker cp local-vi-lang/LanguageToggle.tsx <container>:/app/frontend/src/components/common/LanguageToggle.tsx
docker cp local-vi-lang/add_vi_patch.py <container>:/tmp/add_vi_patch.py
docker compose exec open_notebook python3 /tmp/add_vi_patch.py
docker compose exec open_notebook sh -c "cd /app/frontend && npm ci && npm run build"
docker compose restart open_notebook
```

Xong thì hard-refresh trình duyệt (Cmd/Ctrl + Shift + R) → sidebar → **Language → Tiếng Việt**.

## 🤖 Model đang dùng (gợi ý)

Setup này dùng Ollama local:

- Chat: `qwen3:8b` (có thinking — trả lời kỹ nhưng chậm ~10s/câu)
- Embedding: `nomic-embed-text`

Muốn nhanh hơn: giữ model warm bằng `OLLAMA_KEEP_ALIVE=30m`
(đã set trong LaunchAgent trên máy tác giả), hoặc đổi chat model
không-thinking như `llama3.1:8b`.

## 📁 Lưu ý

- `notebook_data/`, `surreal_data/`, `.env` **không commit** (xem `.gitignore`) —
  clone repo về là chạy mới hoàn toàn, dữ liệu cũ không đi theo.
- Đừng chạy `docker compose down -v` nếu không muốn mất DB local.
- Muốn về image gốc: `mv docker-compose.override.yml docker-compose.override.yml.disabled`
  rồi `docker compose up -d`.

## 🔗 Liên quan
- Repo này: https://github.com/quyen2867/open-notebook
