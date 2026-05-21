import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="Meeting Moderator AI",
    page_icon="🎙️",
    layout="wide"
)

# ─────────────────────────────────────────
# FUNGSI TAMPIL ANALISIS (harus di atas)
# ─────────────────────────────────────────
def tampilkan_analisis(analisis):
    st.divider()
    st.subheader("📊 Hasil Analisis")

    st.markdown("### 💡 Ringkasan")
    st.info(analisis.get("ringkasan", "-"))

    topik = analisis.get("topik_utama", [])
    if topik:
        st.markdown("### 🏷️ Topik Utama")
        cols = st.columns(len(topik))
        for i, t in enumerate(topik):
            cols[i].success(t)

    st.markdown("### 🗣️ Argumen Utama")
    for arg in analisis.get("argumen_utama", []):
        posisi = arg.get("posisi", "netral")
        icon = "🟢" if posisi == "pro" else "🔴" if posisi == "kontra" else "🟡"
        st.markdown(f"{icon} **{posisi.upper()}** — {arg.get('poin', '')}")

    konflik = analisis.get("konflik", [])
    if konflik:
        st.markdown("### ⚡ Konflik & Perdebatan")
        for k in konflik:
            with st.expander(f"Isu: {k.get('isu', '')}"):
                col1, col2 = st.columns(2)
                col1.success(f"**Pro:** {k.get('pihak_pro', '-')}")
                col2.error(f"**Kontra:** {k.get('pihak_kontra', '-')}")

    keputusan = analisis.get("keputusan", [])
    if keputusan:
        st.markdown("### ✅ Keputusan")
        for k in keputusan:
            st.markdown(f"- {k}")

    st.markdown("### 📋 Action Items")
    for item in analisis.get("action_items", []):
        st.markdown(
            f"- **{item.get('tugas', '')}** "
            f"_(tenggat: {item.get('tenggat', 'tidak disebutkan')})_"
        )

    st.markdown("### 🎯 Rekomendasi Moderator")
    st.warning(analisis.get("rekomendasi_moderator", "-"))


# ─────────────────────────────────────────
# NAVIGASI
# ─────────────────────────────────────────
page = st.sidebar.radio("📌 Menu", ["🎙️ Analisis Baru", "📁 History Rapat"])

# ─────────────────────────────────────────
# PAGE 1: ANALISIS BARU
# ─────────────────────────────────────────
if page == "🎙️ Analisis Baru":
    st.title("🎙️ Meeting Moderator AI")
    st.caption("Upload rekaman rapat → Dapat analisis lengkap otomatis")

    uploaded_file = st.file_uploader(
        "Upload file audio rekaman rapat",
        type=["mp3", "wav", "m4a", "ogg", "webm"]
    )

    if uploaded_file:
        st.audio(uploaded_file)

        if st.button("🚀 Analisis Sekarang", type="primary"):
            with st.spinner("⏳ Memproses audio... (bisa 30-60 detik)"):
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                resp = requests.post(f"{API_URL}/transcribe", files=files)

            if resp.status_code != 200:
                st.error(f"Gagal: {resp.text}")
                st.stop()

            data = resp.json()
            transkrip = data["transkrip"]
            durasi = data["durasi_detik"]
            analisis = data["analisis"]

            st.success(f"✅ Selesai! ({durasi:.1f} detik audio diproses)")

            with st.expander("📄 Lihat transkrip lengkap"):
                st.write(transkrip)

            tampilkan_analisis(analisis)

            st.download_button(
                label="⬇️ Download Hasil (JSON)",
                data=json.dumps(analisis, ensure_ascii=False, indent=2),
                file_name="hasil_analisis.json",
                mime="application/json"
            )

# ─────────────────────────────────────────
# PAGE 2: HISTORY
# ─────────────────────────────────────────
elif page == "📁 History Rapat":
    st.title("📁 History Rapat")

    resp = requests.get(f"{API_URL}/history")
    if resp.status_code != 200:
        st.error("Gagal load history")
        st.stop()

    meetings = resp.json()

    if not meetings:
        st.info("Belum ada rapat yang dianalisis.")
    else:
        for m in meetings:
            with st.expander(f"📅 {m['created_at']} — {m['filename']}"):
                st.write(f"**Ringkasan:** {m['ringkasan']}")
                st.write(f"**Durasi:** {m['durasi_detik']} detik")
                if st.button("Lihat Detail", key=f"detail_{m['id']}"):
                    resp2 = requests.get(f"{API_URL}/history/{m['id']}")
                    detail = resp2.json()
                    tampilkan_analisis(detail["analisis"])