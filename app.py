import streamlit as st

st.set_page_config(page_title="Adnan Bahçe Asistanı", page_icon="🌱", layout="wide")

st.title("🌱 Adnan Bahçe Asistanı")
st.write("Bahçe takip, sulama, gübre ve gelişim sistemi")

urunler = [
    "Mısır", "Domates", "Biber", "Çilek", "Salatalık",
    "Kabak", "Bamya", "Karpuz", "Patlıcan"
]

st.subheader("📌 Bugün Ne Yapmalıyım?")

st.info("Dün amino asit uygulandıysa bugün yeni gübre yükleme. Hava kapalı ve toprak nemliyse sulamayı ertele.")

st.subheader("🌿 Ürünlerim")

cols = st.columns(3)

for i, urun in enumerate(urunler):
    with cols[i % 3]:
        st.container(border=True)
        st.markdown(f"### {urun}")
        st.write("Durum: Takip ediliyor")
        st.write("Son sulama: Kontrol edilecek")
        st.write("Son gübre: Kayıt bekleniyor")

st.subheader("📝 Günlük Kayıt Ekle")

urun = st.selectbox("Ürün seç", urunler)
islem = st.selectbox("İşlem seç", ["Sulama", "Gübre", "İlaçlama", "Fotoğraf", "Gözlem"])
notlar = st.text_area("Not yaz", placeholder="Örn: Dün amino asit verdim, toprak nemli...")
foto = st.file_uploader("Fotoğraf yükle", type=["jpg", "jpeg", "png"])

if st.button("Kaydet"):
    st.success(f"{urun} için {islem} kaydı alındı.")
    if notlar:
        st.write("Not:", notlar)
    if foto:
        st.image(foto, caption=f"{urun} fotoğrafı", use_container_width=True)

st.subheader("📸 Fotoğraf Analizi")

analiz_foto = st.file_uploader("Analiz için fotoğraf yükle", type=["jpg", "jpeg", "png"], key="analiz")

if analiz_foto:
    st.image(analiz_foto, caption="Yüklenen fotoğraf", use_container_width=True)

    if st.button("Basit Analiz Yap"):
        st.success("Fotoğraf alındı.")
        st.write("Şimdilik demo analiz:")
        st.write("- Bitki genel kontrol edilmeli.")
        st.write("- Yaprak rengi ve zararlı için yakın fotoğraf daha iyi olur.")
        st.write("- Son gübre/sulama kaydıyla birlikte değerlendirme yapılmalı.")
