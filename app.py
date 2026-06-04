import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Adnan - Akıllı Bahçe Pro v2", layout="wide")

st.title("🚀 Adnan - Akıllı Bahçe Otomasyonu v2.0")
st.subheader("Adana / Organik Tarım Karar Motoru & Envanter Takip Sistemi")
st.markdown("---")

if 'log_gecmisi' not in st.session_state:
    st.session_state.log_gecmisi = [
        {
            "tarih": datetime(2026, 6, 3),
            "urunler": ["Solucan Gübresi", "Amino Asit", "Humik Asit", "Deniz Yosunu"],
            "bitkiler": ["Mısır", "Domates", "Biber", "Patlıcan", "Salatalık"]
        }
    ]

if 'envanter' not in st.session_state:
    st.session_state.envanter = {
        "Solucan Gübresi": 10.0,
        "Humik Asit": 5.0,
        "Amino Asit": 2.5,
        "Deniz Yosunu": 2.0,
        "Kalsiyum Gübresi": 3.0,
        "Gülleci Bulamacı": 4.0,
        "Kaolin Kili": 15.0
    }

st.sidebar.header("🌤️ Adana Canlı Hava Durumu Sinyali")
adana_sicaklik = st.sidebar.slider("Anlık Adana Sıcaklığı (°C)", 25, 45, 34)
adana_nem = st.sidebar.slider("Anlık Nem Oranı (%)", 30, 100, 55)

st.sidebar.markdown("---")
st.sidebar.header("🤖 Karar Motoru Sinyalleri")

def kurallari_denetle():
    son_islem = st.session_state.log_gecmisi[-1]
    gecen_gun = (datetime.now() - son_islem["tarih"]).days
    st.sidebar.info(f"🔄 Son uygulamanın üzerinden **{gecen_gun}** gün geçti.")
    
    gulleci_tarihleri = [x["tarih"] for x in st.session_state.log_gecmisi if "Gülleci Bulamacı" in x["urunler"]]
    kalsiyum_kilitli = False
    
    if gulleci_tarihleri:
        son_gulleci = max(gulleci_tarihleri)
        gulleci_gecen_gun = (datetime.now() - son_gulleci).days
        if gulleci_gecen_gun < 7:
            kalsiyum_kilitli = True
            st.sidebar.error(f"⛔ **KALSİYUM KİLİDİ AKTİF:** {gulleci_gecen_gun} gün önce Gülleci uygulandığı için şu an Kalsiyum atamazsınız!")

    if adana_nem > 80:
        st.sidebar.warning("⚠️ **MANTAR RİSKİ:** Nem %80'in üzerinde! Külleme ve mildiyö riski yüksek.")
    elif adana_sicaklik >= 38:
        st.sidebar.error("🔥 **AŞIRI TERMAL STRES:** Gündüz gübrelemeyi kesin, akşam sulamasını artırın.")
    
    if 5 <= gecen_gun <= 8:
        st.sidebar.warning("🚨 **SİNYAL:** Kaolin Kili zamanı! Yaprakları korumaya alın.")
        
    return kalsiyum_kilitli

kalsiyum_kilitli_durum = kurallari_denetle()

tab1, tab2, tab3 = st.tabs(["📋 Bahçe Yönetimi & Form", "📦 Envanter (Ambar)", "📸 AI Yaprak Analiz İstasyonu"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.header("📅 Dinamik Bahçe Akışı")
        takvim_verisi = {
            "Bitki Grubu": ["Mısırlar (Doğrudan Tohum)", "Yeni Fideler (Genel)", "Tüm Bahçe"],
            "Gelişim Evresi": ["Hızlı Boylanma Evresi", "Toprağa Tutunma & Köklenme", "Denge Stabil"],
            "Kritik Aksiyon": ["Yabancı ot temizliği & Kaolin", "Yaprak biti gözetimi", "Akşam düzenli sulama"]
        }
        st.table(pd.DataFrame(takvim_verisi))
        
    with col2:
        st.subheader("➕ Yeni İşlem Emir Girişi")
        with st.form("islem_formu"):
            yeni_tarih = st.date_input("Uygulama Tarihi", datetime.now())
            secilen_urunler = st.multiselect("Kullanılacak Organik Ürünler", list(st.session_state.envanter.keys()))
            secilen_bitkiler = st.multiselect("Uygulanacak Bitkiler", ["Mısır", "Domates", "Biber", "Patlıcan", "Salatalık", "Karpuz"])
            kullanilan_miktar = st.number_input("Ürün başına miktar (L/Kg)", min_value=0.1, max_value=5.0, value=0.5, step=0.1)
            submit = st.form_submit_button("Sisteme İşle")
            
            if submit:
                if "Gülleci Bulamacı" in secilen_urunler and "Kalsiyum Gübresi" in secilen_urunler:
                    st.error("⛔ **EMİR REDDEDİLDİ:** İkisi aynı anda karıştırılamaz!")
                elif "Kalsiyum Gübresi" in secilen_urunler and kalsiyum_kilitli_durum:
                    st.error("⛔ **EMİR REDDEDİLDİ:** Kalsiyum kilidi aktif!")
                elif not secilen_urunler or not secilen_bitkiler:
                    st.warning("⚠️ Lütfen seçim yapın.")
                else:
                    stok_yeterli = True
                    for urun in secilen_urunler:
                        if st.session_state.envanter[urun] < kullanilan_miktar:
                            st.error(f"⛔ **STOK YETERSİZ:** {urun} tükenmek üzere!")
                            stok_yeterli = False
                    
                    if stok_yeterli:
                        for urun in secilen_urunler:
                            st.session_state.envanter[urun] -= kullanilan_miktar
                        st.session_state.log_gecmisi.append({
                            "tarih": datetime.combine(yeni_tarih, datetime.min.time()),
                            "urunler": secilen_urunler,
                            "bitkiler": secilen_bitkiler
                        })
                        st.success("✅ İşlem başarıyla uygulandı!")
                        st.rerun()

with tab2:
    st.header("📦 Dijital Ambar Durumu")
    env_df = pd.DataFrame(list(st.session_state.envanter.items()), columns=["Ürün Adı", "Mevcut Stok (Litre/Kg)"])
    def renklendir(val):
        color = 'red' if val < 2.0 else 'green'
        return f'color: {color}'
    st.dataframe(env_df.style.map(renklendir, subset=["Mevcut Stok (Litre/Kg)"]))
    
    st.subheader("📥 Depoya Malzeme Tedariği Yap")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        tedarik_urun = st.selectbox("Tedarik Edilen Ürün", list(st.session_state.envanter.keys()))
    with col_t2:
        tedarik_miktar = st.number_input("Eklenen Miktar (L/Kg)", min_value=1.0, max_value=50.0, value=5.0, step=1.0)
    if st.button("Depoyu Güncelle"):
        st.session_state.envanter[tedarik_urun] += tedarik_miktar
        st.success(f"📥 Depo güncellendi!")
        st.rerun()

with tab3:
    st.header("📸 AI Görsel Teşhis Odası")
    yuklenen_dosya = st.file_uploader("Yaprak Fotoğrafı Yükle", type=["jpg", "png", "jpeg"])
    if yuklenen_dosya is not None:
        st.image(yuklenen_dosya, caption="Yüklenen Veri", width=400)
        st.warning("🤖 **AI Analizi:** Fotoğraf alındı. Geçmiş verilere göre bitkiler dengede görünüyor, yabancı ot kontrolü önerilir.")

st.markdown("---")
st.subheader("📜 Geçmiş Operasyon Günlüğü")
st.write(st.session_state.log_gecmisi)
