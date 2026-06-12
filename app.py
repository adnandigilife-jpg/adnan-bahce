import os
import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Adnan Bahçe Asistanı",
    page_icon="🌱",
    layout="wide"
)

DB_PATH = "bahce_kayitlari.db"
PHOTO_DIR = Path("fotograflar")
PHOTO_DIR.mkdir(exist_ok=True)

URUNLER = [
    "Mısır", "Domates", "Biber", "Çilek", "Salatalık",
    "Kabak", "Bamya", "Karpuz", "Patlıcan"
]

ISLEMLER = [
    "Sulama",
    "Gübre",
    "İlaçlama",
    "Fotoğraf",
    "Gözlem",
    "Hasat"
]


def db_baglan():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def tablo_olustur():
    conn = db_baglan()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kayitlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT NOT NULL,
            urun TEXT NOT NULL,
            islem TEXT NOT NULL,
            miktar TEXT,
            notlar TEXT,
            foto_yolu TEXT,
            kayit_zamani TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def kayit_ekle(tarih, urun, islem, miktar, notlar, foto_yolu):
    conn = db_baglan()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO kayitlar
        (tarih, urun, islem, miktar, notlar, foto_yolu, kayit_zamani)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(tarih),
        urun,
        islem,
        miktar,
        notlar,
        foto_yolu,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


def kayitlari_getir():
    conn = db_baglan()
    df = pd.read_sql_query(
        "SELECT * FROM kayitlar ORDER BY tarih DESC, id DESC",
        conn
    )
    conn.close()
    return df


def kayit_sil(kayit_id):
    conn = db_baglan()
    cur = conn.cursor()
    cur.execute("DELETE FROM kayitlar WHERE id = ?", (kayit_id,))
    conn.commit()
    conn.close()


def foto_kaydet(uploaded_file, urun, tarih):
    if uploaded_file is None:
        return ""

    ext = uploaded_file.name.split(".")[-1]
    temiz_urun = urun.lower().replace("ı", "i").replace(" ", "_")
    dosya_adi = f"{tarih}_{temiz_urun}_{datetime.now().strftime('%H%M%S')}.{ext}"
    yol = PHOTO_DIR / dosya_adi

    with open(yol, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(yol)


def basit_oneri(df):
    oneriler = []

    bugun = date.today().isoformat()

    for urun in URUNLER:
        urun_df = df[df["urun"] == urun] if not df.empty else pd.DataFrame()

        if urun_df.empty:
            oneriler.append((urun, "Kayıt yok", "Bu ürün için ilk kayıt girilmeli."))
            continue

        son_kayit = urun_df.iloc[0]
        son_islem = son_kayit["islem"]
        son_tarih = son_kayit["tarih"]

        gun_farki = (date.today() - datetime.strptime(son_tarih, "%Y-%m-%d").date()).days

        if son_islem == "Gübre" and gun_farki <= 2:
            oneriler.append((urun, "Bekle", "Son gübre uygulaması yeni. Üst üste yükleme yapma."))
        elif son_islem == "Sulama" and gun_farki <= 1:
            oneriler.append((urun, "Su verme", "Son sulama yakın. Toprak nemini kontrol et."))
        elif gun_farki >= 5:
            oneriler.append((urun, "Kontrol et", "Bu ürün için birkaç gündür kayıt yok. Gözlem yap."))
        else:
            oneriler.append((urun, "Normal", "Kayıtlara göre acil işlem görünmüyor."))

    return oneriler


tablo_olustur()

st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 50%, #fff7ed 100%);
}
.block-container {
    padding-top: 2rem;
}
.big-card {
    background: rgba(255,255,255,0.85);
    padding: 24px;
    border-radius: 24px;
    border: 1px solid rgba(34,197,94,0.18);
    box-shadow: 0 10px 30px rgba(20,83,45,0.08);
}
.small-card {
    background: white;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid #dcfce7;
    box-shadow: 0 5px 18px rgba(20,83,45,0.05);
}
</style>
""", unsafe_allow_html=True)

st.title("🌱 Adnan Bahçe Asistanı")
st.caption("Sulama, gübre, ilaç, fotoğraf, gözlem ve hasat kayıt sistemi")

df = kayitlari_getir()

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Kayıt Ekle",
    "📋 Geçmiş Kayıtlar",
    "📌 Bugün Ne Yapmalıyım?",
    "📸 Fotoğraf Arşivi"
])

with tab1:
    st.subheader("➕ Yeni Bahçe Kaydı")

    col1, col2, col3 = st.columns(3)

    with col1:
        tarih = st.date_input("Tarih", value=date.today())

    with col2:
        urun = st.selectbox("Ürün", URUNLER)

    with col3:
        islem = st.selectbox("İşlem", ISLEMLER)

    miktar = st.text_input("Miktar / Ölçü", placeholder="Örn: 100 ml amino asit, 70 litre su, 350 ml Calpower-B")

    notlar = st.text_area(
        "Not",
        placeholder="Örn: Dün amino asit verdim, toprak nemli, yapraklar iyi..."
    )

    foto = st.file_uploader("Fotoğraf ekle", type=["jpg", "jpeg", "png"])

    if st.button("✅ Kaydı Kaydet", use_container_width=True):
        foto_yolu = foto_kaydet(foto, urun, tarih)
        kayit_ekle(tarih, urun, islem, miktar, notlar, foto_yolu)
        st.success("Kayıt kalıcı olarak kaydedildi. Siteyi kapatıp açsan da duracak.")
        st.rerun()

with tab2:
    st.subheader("📋 Geçmiş Kayıtlar")

    if df.empty:
        st.info("Henüz kayıt yok.")
    else:
        filtre_urun = st.selectbox("Ürüne göre filtrele", ["Tümü"] + URUNLER, key="filtre_urun")
        filtre_islem = st.selectbox("İşleme göre filtrele", ["Tümü"] + ISLEMLER, key="filtre_islem")

        goster = df.copy()

        if filtre_urun != "Tümü":
            goster = goster[goster["urun"] == filtre_urun]

        if filtre_islem != "Tümü":
            goster = goster[goster["islem"] == filtre_islem]

        st.dataframe(
            goster[["id", "tarih", "urun", "islem", "miktar", "notlar", "kayit_zamani"]],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.subheader("🗑️ Kayıt Sil")

        sil_id = st.number_input("Silinecek kayıt ID", min_value=1, step=1)

        if st.button("Sil"):
            kayit_sil(int(sil_id))
            st.warning("Kayıt silindi.")
            st.rerun()

with tab3:
    st.subheader("📌 Bugün Ne Yapmalıyım?")

    if df.empty:
        st.info("Öneri için önce birkaç kayıt girmen lazım.")
    else:
        oneriler = basit_oneri(df)

        for urun, durum, detay in oneriler:
            if durum in ["Bekle", "Su verme"]:
                st.warning(f"**{urun}** → {durum}: {detay}")
            elif durum == "Kontrol et":
                st.info(f"**{urun}** → {durum}: {detay}")
            else:
                st.success(f"**{urun}** → {durum}: {detay}")

with tab4:
    st.subheader("📸 Fotoğraf Arşivi")

    if df.empty or df["foto_yolu"].fillna("").eq("").all():
        st.info("Henüz fotoğraf kaydı yok.")
    else:
        foto_df = df[df["foto_yolu"].fillna("") != ""]

        for _, row in foto_df.iterrows():
            st.markdown(f"### {row['urun']} - {row['tarih']}")
            st.write(f"**İşlem:** {row['islem']}")
            st.write(f"**Miktar:** {row['miktar']}")
            st.write(f"**Not:** {row['notlar']}")

            if os.path.exists(row["foto_yolu"]):
                image = Image.open(row["foto_yolu"])
                st.image(image, use_container_width=True)

            st.divider()
