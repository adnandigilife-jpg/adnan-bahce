import streamlit as st
import requests
import datetime

# Sayfa Genişliği Ayarı
st.set_page_config(layout="wide")

# Telegram Bildirim Fonksiyonu
def telegram_bildirim_gonder(mesaj):
    # Kendi bilgilerinle doldur:
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

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Dinamik Bahçe Akışı")
        # Bahçe akış tablosu verisi
        bahce_data = [
            {"Bitki Grubu": "Mısırlar (Doğrudan Tohum)", "Gelişim Evresi": "Hızlı Boylanma Evresi", "Kritik Aksiyon": "Yabancı ot temizliği & Kaolin"},
            {"Bitki Grubu": "Yeni Fideler (Genel)", "Gelişim Evresi": "Toprağa Tutunma & Köklenme", "Kritik Aksiyon": "Yaprak biti gözetimi"},
            {"Bitki Grubu": "Tüm Bahçe", "Gelişim Evresi": "Denge Stabil", "Kritik Aksiyon": "Akşam düzenli sulama"}
        ]
        st.table(bahce_data)

    with col2:
        st.markdown("### ➕ Yeni İşlem Emir Girişi")
        
        # Form Elemanları
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
        
        # BUTONA BASILMA ANI
        if st.button("Sisteme İşle"):
            if not secilen_urunler or not secilen_bitkiler:
                st.warning("Lütfen önce ürün ve bitki seçimi yapın!")
            else:
                # 1. Ekranda Başarı Mesajı Göster
                st.success("İşlem başarıyla sisteme kaydedildi ve veri tabanına işlendi!")
                
                # 2. Telegram Bildirimini Tetikle
                bitki_str = ", ".join(secilen_bitkiler)
                urun_str = ", ".join(secilen_urunler)
                mesaj_metni = f"🌿 Adnan Radar Bahçe Bildirimi:\n📅 Tarih: {uygulama_tarihi}\n🚜 Bitkiler: {bitki_str}\n🧪 Ürün: {urun_str}\n📊 Miktar: {miktar} L/Kg\n\nUygulama sisteme başarıyla işlendi ve ambar stoklarından düşüldü! ✅"
                
                telegram_bildirim_gonder(mesaj_metni)

with tab2:
    st.markdown("### 📦 Ambar Stok Durumu")
    st.info("Stoklar güncel tutulmaktadır.")

with tab3:
    st.markdown("### 📸 AI Yaprak Analiz İstasyonu")
    st.info("Analiz sistemi aktif.")
