# Meeting Moderator AI

Aplikasi asisten moderator rapat pintar berbasis AI untuk mentranskripsikan rekaman audio rapat dan menganalisis dinamika diskusi secara otomatis, mendalam, dan terstruktur.

---

## Fitur Utama

- **Transkripsi Audio Cepat & Akurat (STT):**
  - Menggunakan model **Whisper Large v3** via Groq API dengan dukungan bahasa Indonesia (`id`).
  - Mendukung berbagai format audio: `.mp3`, `.wav`, `.m4a`, `.ogg`, `.webm`.

- **Analisis Diskusi Mendalam (LLM):**
  - Menggunakan model **Qwen 3.8 27B** via Groq API.
  - **Ringkasan Rapat:** Rangkuman inti diskusi 2–3 kalimat.
  - **Topik Utama:** Ekstraksi poin-poin bahasan utama.
  - **Argumen & Posisi:** Pemetaan argumen ke kategori *PRO*, *KONTRA*, atau *NETRAL*.
  - **Deteksi Konflik & Perdebatan:** Memetakan isu yang diperdebatkan beserta pandangan masing-masing pihak.
  - **Keputusan & Kesepakatan:** Daftar butir keputusan yang disepakati.
  - **Action Items:** Daftar tugas tindak lanjut beserta tenggat waktu (*deadline*).
  - **Rekomendasi Moderator:** Saran langkah berikutnya dari sudut pandang fasilitator/moderator profesional.

- **Riwayat Rapat (History):**
  - Penyimpanan riwayat rapat, transkrip, dan hasil analisis secara persisten di database SQLite.
  - Fitur peninjauan kembali hasil analisis rapat terdahulu.

- **Ekspor Data:**
  - Unduh hasil analisis terstruktur dalam format file JSON.

---

## Tech Stack

| Komponen | Teknologi / Library |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) |
| **Frontend UI** | [Streamlit](https://streamlit.io/) |
| **Database & ORM** | SQLite & [SQLAlchemy](https://www.sqlalchemy.org/) |
| **AI Models (Groq Cloud)** | `whisper-large-v3` (STT) & `qwen/qwen3.8-27b` (LLM) |

---

## Struktur Proyek

```plaintext
meeting-moderator/
├── backend/
│   ├── models/
│   │   └── database.py          # Konfigurasi SQLAlchemy model & koneksi SQLite
│   ├── routes/
│   │   ├── analyze.py           # Endpoint analisis teks transkrip
│   │   ├── history.py           # Endpoint riwayat dan detail rapat
│   │   └── transcribe.py        # Endpoint upload audio, STT, & auto-analysis
│   ├── services/
│   │   ├── llm_service.py       # Integrasi prompt moderator ke Groq LLM
│   │   └── stt_service.py       # Integrasi transkripsi audio ke Groq Whisper
│   └── main.py                  # Entrypoint FastAPI & registrasi router
├── frontend/
│   └── app.py                   # Antarmuka web Streamlit
├── uploads/                     # Direktori sementara penyimpanan berkas audio
├── .env.example                 # Template variabel lingkungan
├── meeting_moderator.db         # Database SQLite lokal
└── requirements.txt             # Dependensi Python
```

---

## Panduan Instalasi & Menjalankan

### 1. Clone Repositori & Masuk ke Folder Proyek

```bash
git clone https://github.com/fazaradit/meeting-moderator.git
cd meeting-moderator
```

### 2. Buat & Aktifkan Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalasi Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Variabel Lingkungan (`.env`)

Salin berkas `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

Buka berkas `.env` dan masukkan API Key dari Groq:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> Dapatkan API key di [Groq Console](https://console.groq.com/keys).

---

## Menjalankan Aplikasi

Jalankan backend API dan frontend UI di terminal terpisah (pastikan virtual environment aktif di kedua terminal):

### Terminal 1 — Backend (FastAPI)

```bash
uvicorn backend.main:app --reload --port 8000
```
- API Docs (Swagger UI): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/`

### Terminal 2 — Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```
- Buka antarmuka web di browser: `http://localhost:8501`

---

## Dokumentasi Endpoint API

| Method | Endpoint | Deskripsi |
| :--- | :--- | :--- |
| `GET` | `/` | Root health check |
| `POST` | `/api/transcribe` | Upload file audio, proses STT, analisis, dan simpan ke DB |
| `POST` | `/api/analyze` | Analisis teks transkrip langsung (JSON input `{ "transkrip": "..." }`) |
| `GET` | `/api/history` | Mengambil daftar riwayat seluruh rapat |
| `GET` | `/api/history/{id}` | Mengambil detail riwayat rapat dan hasil analisis berdasarkan ID |
