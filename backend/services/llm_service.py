import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT_TEMPLATE = """
Kamu adalah AI moderator diskusi profesional. Analisis transkrip rapat berikut secara mendalam.

TRANSKRIP:
{transkrip}

Berikan analisis dalam format JSON berikut (HANYA JSON, tanpa teks lain, tanpa markdown):
{{
  "ringkasan": "ringkasan singkat isi diskusi dalam 2-3 kalimat",
  "topik_utama": ["topik 1", "topik 2"],
  "argumen_utama": [
    {{"poin": "argumen atau pendapat penting", "posisi": "pro/kontra/netral"}}
  ],
  "konflik": [
    {{"isu": "isu yang diperdebatkan", "pihak_pro": "argumen mendukung", "pihak_kontra": "argumen menolak"}}
  ],
  "keputusan": ["keputusan yang disepakati dalam rapat"],
  "action_items": [
    {{"tugas": "apa yang harus dilakukan", "tenggat": "kapan jika disebutkan"}}
  ],
  "rekomendasi_moderator": "saran tindak lanjut dari sudut pandang moderator"
}}
"""

def analyze_transcript(transkrip: str) -> dict:
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "system",
                "content": "Kamu adalah AI moderator diskusi. Selalu jawab HANYA dengan JSON valid, tanpa teks tambahan."
            },
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(transkrip=transkrip)
            }
        ],
        temperature=0.3,
        max_tokens=2000
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    return json.loads(raw)