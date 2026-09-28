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

## 📖 Cách dùng

1. **Cấu hình model** — sidebar → **Models**: thêm provider (Ollama local
   hoặc API key cloud như OpenAI/Groq/Gemini), bấm **Sync Models**,
   rồi gán model mặc định: **Chat** (trả lời), **Embedding** (tìm kiếm),
   **TTS/STT** (podcast). Chạy Ollama trên máy host thì base URL là
   `http://host.docker.internal:11434`.
2. **Tạo Notebook** — nút **New Notebook**: mỗi notebook là một chủ đề,
   gom các nguồn + ghi chú liên quan.
3. **Thêm nguồn (Sources)** — **New Source**: dán URL, tải file
   (PDF/DOC/ảnh/audio) hoặc dán text. Đợi trạng thái **Completed**;
   bật **embedding** để AI tìm kiếm theo ngữ nghĩa.
4. **Chat với nguồn** — mở notebook, chat ở khung bên: câu trả lời
   dựa trên các nguồn đang bật context (bấm vào nguồn để đổi chế độ
   full/insights/tắt).
5. **Ask and Search** — hỏi đáp trên toàn bộ knowledge base;
   chọn **Text search** (từ khoá) hoặc **Vector search** (ngữ nghĩa,
   cần embedding model).
6. **Transformations** — biến nguồn thành insight: tóm tắt, trích ý chính...
   Chạy trên từng nguồn, kết quả lưu thành note.
7. **Podcasts** — tạo tập podcast từ nội dung: cần **Speaker profile**
   (giọng, TTS model) + **Episode profile** (kịch bản) trước, rồi **Generate**.
8. **Đổi tiếng Việt** — cuối sidebar → **Language → Tiếng Việt**.

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
