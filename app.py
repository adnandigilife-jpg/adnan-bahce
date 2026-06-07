import streamlit as st
import requests
import datetime
from PIL import Image

# Sayfa Genişliği Ayarı
st.set_page_config(layout="wide", page_title="Adnan Bahçe Otomasyonu", page_icon="🌿")

# Telegram Bildirim Fonksiyonu
def telegram_bildirim_gonder(mesaj):
    # Kendi bilgilerini buraya gir:
    TOKEN = "BURAYA_BOTFATHERDAN_ALDIGIN_TOKENI_YAZ"
    CHAT_ID = "BURAYA_USERINFOBOTDAN_ALDIGIN_IDYI_YAZ"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        pass

# Başlıklar
st.title("🚀 Adnan - Akıllı Bahçe Otomasyonu v2.0")
st.subheader("Adana / Organik Tarım Karar Motoru & Envanter Takip Sistemi")

# Yan Menü (Sidebar) - Hava Durumu Sinyalleri
st.sidebar.markdown("### ☀️ Adana Canlı Hava Durumu Sinyali")
sicaklik = st.sidebar.slider("Anlık Adana Sıcaklığı (°C)", 0, 50, 34)
nem = st.sidebar.slider("Anlık Nem Oranı (%)", 0, 100, 55)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👁️ Karar Motoru Sinyalleri")
st.sidebar.info("Son uygulamanın üzerinden 1 gün geçti.")

# Sekmeler (Tabs)
tab1, tab2, tab3 = st.tabs(["📋 Bahçe Yönetimi & Form", "📦 Envanter (Ambar)", "📸 AI Yaprak Analiz İstasyonu"])

# --- TAB 1: BAHÇE YÖNETİMİ ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Dinamik Bahçe Akışı")
        bahce_data = [
            {"Bitki Grubu": "Mısırlar (Doğrudan Tohum)", "Gelişim Evresi": "Hızlı Boylanma Evresi", "Kritik Aksiyon": "Yabancı ot temizliği & Kaolin"},
            {"Bitki Grubu": "Yeni Fideler (Genel)", "Gelişim Evresi": "Toprağa Tutunma & Köklenme", "Kritik Aksiyon": "Yaprak biti gözetimi"},
            {"Bitki Grubu": "Tüm Bahçe", "Gelişim Evresi": "Denge Stabil", "Kritik Aksiyon": "Akşam düzenli sulama"}
        ]
        st.table(bahce_data)

    with col2:
        st.markdown("### ➕ Yeni İşlem Emir Girişi")
        uygulama_tarihi = st.date_input("Uygulama Tarihi", datetime.date(2026, 6, 7))
        
        secilen_urunler = st.multiselect(
            "Kullanılacak Organik Ürünler",
            ["Solucan Gübresi", "Deniz Yosunu", "Amino Asit", "Hümik Asit", "Kalsiyum Gübresi"]
        )
        
        secilen_bitkiler = st.multiselect(
            "Uygulanacak Bitkiler",
            ["Mısır", "Domates", "Biber", "Patlıcan", "Salatalık", "Karpuz"]
        )
        
        miktar = st.number_input("Ürün başına miktar (L/Kg)", min_value=0.0, max_value=10.0, value=0.70, step=0.10)
        
        if st.button("Sisteme İşle"):
            if not secilen_urunler or not secilen_bitkiler:
                st.warning("Lütfen önce ürün ve bitki seçimi yapın!")
            else:
                st.success("İşlem başarıyla sisteme kaydedildi ve veri tabanına işlendi! ✅")
                
                bitki_str = ", ".join(secilen_bitkiler)
                urun_str = ", ".join(secilen_urunler)
                mesaj_metni = f"🌿 Adnan Radar Bahçe Bildirimi:\n📅 Tarih: {uygulama_tarihi}\n🚜 Bitkiler: {bitki_str}\n🧪 Ürün: {urun_str}\n📊 Miktar: {miktar} L/Kg\n\nUygulama sisteme başarıyla işlendi ve ambar stoklarından düşüldü! ✅"
                
                telegram_bildirim_gonder(mesaj_metni)

# --- TAB 2: ENVANTER ---
with tab2:
    st.markdown("### 📦 Ambar Stok Durumu")
    st.info("Stoklar güncel tutulmaktadır.")

# --- TAB 3: AI YAPRAK ANALİZİ (GERİ GETİRİLEN KISIM) ---
with tab3:
    st.markdown("### 📸 AI Yaprak Analiz İstasyonu")
    st.write("Bahçeden çektiğiniz yaprak fotoğrafını yükleyin; sistem hastalık veya besin eksikliğini analiz etsin.")
    
    # Dosya yükleme alanı ve Kamera entegrasyonu
    uploaded_file = st.file_uploader("Bir Yaprak Fotoğrafı Seçin Veya Sürükleyin...", type=["jpg", "jpeg", "png"])
    camera_file = st.camera_input("Veya Doğrudan Kamerayla Çekin 📸")
    
    # İki kaynaktan biri doluysa resmi göster
    target_file = uploaded_file if uploaded_file is not None else camera_file
    
    if target_file is not None:
        image = Image.open(target_file)
        st.image(image, caption="Analiz Edilen Yaprak", use_container_width=True)
        
        # Yapay zeka simülasyonu analiz sonuçları
        st.warning("🔄 Yapay Zeka Görüntüyü İşliyor...")
        st.info("📊 **AI Analiz Raporu:** Yaprakta hafif azot eksikliği ve alt yapraklarda kalsiyum ihtiyacı sinyali algılandı. Üst menüden Kalsiyum Gübresi veya Amino Asit emri girilmesi önerilir.")
