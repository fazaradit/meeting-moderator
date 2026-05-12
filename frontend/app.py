import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="Meeting Moderator AI",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Meeting Moderator AI")
st.caption("Upload rekaman rapat → Dapat analisis lengkap otomatis")

uploaded_file = st.file_uploader(
    "Upload file audio rekaman rapat",
    type=["mp3", "wav", "m4a", "ogg", "webm"]
)

if uploaded_file:
    st.audio(uploaded_file)

    if st.button("🚀 Analisis Sekarang", type="primary"):

        # STEP 1: Transkripsi
        with st.spinner("⏳ Mengubah audio ke teks..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            resp1 = requests.post(f"{API_URL}/transcribe", files=files)

        if resp1.status_code != 200:
            st.error(f"Gagal transkripsi: {resp1.text}")
            st.stop()

        transkrip = resp1.json()["transkrip"]
        durasi = resp1.json()["durasi_detik"]

        st.success(f"✅ Transkripsi selesai ({durasi:.1f} detik audio)")

        with st.expander("📄 Lihat transkrip lengkap"):
            st.write(transkrip)

        # STEP 2: Analisis AI
        with st.spinner("🧠 AI sedang menganalisis diskusi..."):
            resp2 = requests.post(
                f"{API_URL}/analyze",
                json={"transkrip": transkrip}
            )

        if resp2.status_code != 200:
            st.error(f"Gagal analisis: {resp2.text}")
            st.stop()

        analisis = resp2.json()["analisis"]

        st.divider()
        st.subheader("📊 Hasil Analisis")

        # Ringkasan
        st.markdown("### 💡 Ringkasan")
        st.info(analisis.get("ringkasan", "-"))

        # Topik utama
        st.markdown("### 🏷️ Topik Utama")
        topik = analisis.get("topik_utama", [])
        cols = st.columns(len(topik) if topik else 1)
        for i, t in enumerate(topik):
            cols[i].success(t)

        # Argumen
        st.markdown("### 🗣️ Argumen Utama")
        for arg in analisis.get("argumen_utama", []):
            posisi = arg.get("posisi", "netral")
            icon = "🟢" if posisi == "pro" else "🔴" if posisi == "kontra" else "🟡"
            st.markdown(f"{icon} **{posisi.upper()}** — {arg.get('poin', '')}")

        # Konflik
        konflik = analisis.get("konflik", [])
        if konflik:
            st.markdown("### ⚡ Konflik & Perdebatan")
            for k in konflik:
                with st.expander(f"Isu: {k.get('isu', '')}"):
                    col1, col2 = st.columns(2)
                    col1.success(f"**Pro:** {k.get('pihak_pro', '-')}")
                    col2.error(f"**Kontra:** {k.get('pihak_kontra', '-')}")

        # Keputusan
        keputusan = analisis.get("keputusan", [])
        if keputusan:
            st.markdown("### ✅ Keputusan")
            for k in keputusan:
                st.markdown(f"- {k}")

        # Action Items
        st.markdown("### 📋 Action Items")
        action_items = analisis.get("action_items", [])
        if action_items:
            for item in action_items:
                st.markdown(
                    f"- **{item.get('tugas', '')}** "
                    f"_(tenggat: {item.get('tenggat', 'tidak disebutkan')})_"
                )
        else:
            st.write("Tidak ada action items terdeteksi.")

        # Rekomendasi
        st.markdown("### 🎯 Rekomendasi Moderator")
        st.warning(analisis.get("rekomendasi_moderator", "-"))

        # Download JSON
        st.divider()
        st.download_button(
            label="⬇️ Download Hasil (JSON)",
            data=json.dumps(analisis, ensure_ascii=False, indent=2),
            file_name="hasil_analisis.json",
            mime="application/json"
        )