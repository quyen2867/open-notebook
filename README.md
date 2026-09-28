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

Lần đầu chạy sẽ tự build image local (~10 phút do build frontend) —
các lần sau vào thẳng. Vào sidebar → **Language → Tiếng Việt** là xong.

## 🇻🇳 Việt hoá giao diện

Locale `vi-VN` (963 keys, test parity 34/34 pass) được **build sẵn vào image**
qua `local-sse-fix/Dockerfile` — `docker compose up --build` là có,
không cần làm tay.

Nguồn patch:

- `local-sse-fix/vi-lang/` — file build (`vi-VN/index.ts`, `locales-index.ts`,
  `LanguageToggle.tsx`, `add_vietnamese_key.py`)
- `local-vi-lang/` — bản làm việc + đối chiếu (`en-US-index.ts`, script cũ)

> Chỉ khi dùng image gốc không qua build (ví dụ `docker compose pull`
> image upstream) mới cần áp tay — xem lịch sử commit để lấy các bước cũ.

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
