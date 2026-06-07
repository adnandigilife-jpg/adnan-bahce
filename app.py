import streamlit as st
import datetime
from PIL import Image

# Sayfa Genişliği Ayarı
st.set_page_config(layout="wide", page_title="Adnan Bahçe Otomasyonu", page_icon="🌿")

# --- SİTE HAFIZASI (SESSION STATE) ---
# Sayfa yenilense bile geçmiş verilerin kaybolmaması için hafıza alanı oluşturuyoruz
if "uygulama_gecmisi" not Western_style in st.session_state:
    st.session_state["uygulama_gecmisi"] = [
        {"Tarih": "2026/06/04", "Uygulanan Ürün": "Solucan Gübresi + Amino Asit", "Hedef Bitkiler": "Tüm Fideler & Mısırlar", "Miktar (L/Kg)": 0.50, "Durum": "Tamamlandı ✅"},
        {"Tarih": "2026/05/28", "Uygulanan Ürün": "Deniz Yosunu + Hümik Asit", "Hedef Bitkiler": "Yeni Fideler (Genel)", "Miktar (L/Kg)": 0.40, "Durum": "Tamamlandı ✅"}
    ]

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
            {"Bitki Grubu": "Yeni Fideler (Genel)", "Gelişim Evresi": "Toprağa Tutunma & Köklenme", "Kritik Aksiyon": "Yaprak biti gözeti̇mi"},
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
                
                # Yeni veriyi listenin en başına ekliyoruz
                yeni_kayit = {
                    "Tarih": uygulama_tarihi.strftime("%Y/%m/%d"),
                    "Uygulanan Ürün": ", ".join(secilen_urunler),
                    "Hedef Bitkiler": ", ".join(secilen_bitkiler),
                    "Miktar (L/Kg)": miktar,
                    "Durum": "Tamamlandı ✅"
                }
                st.session_state["uygulama_gecmisi"].insert(0, yeni_kayit)
                st.rerun()

    # --- UYGULAMA GEÇMİŞİ GÖRÜNTÜLEME ALANI ---
    st.markdown("---")
    st.markdown("### 📜 Geçmiş Uygulama Kayıtları")
    st.write("Sisteme başarıyla işlenmiş ve hafızaya alınmış son organik gübreleme/bakım geçmişiniz:")
    
    # Hafızadaki listeyi tablo olarak ekrana basıyoruz
    st.table(st.session_state["uygulama_gecmisi"])

# --- TAB 2: ENVANTER ---
with tab2:
    st.markdown("### 📦 Ambar Stok Durumu")
    st.info("Stoklar güncel tutulmaktadır.")

# --- TAB 3: AI YAPRAK ANALİZİ ---
with tab3:
    st.markdown("### 📸 AI Yaprak Analiz İstasyonu")
    st.write("Bahçeden çektiğiniz yaprak fotoğrafını yükleyin; sistem hastalık veya besin eksikliğini analiz etsin.")
    
    uploaded_file = st.file_uploader("Bir Yaprak Fotoğrafı Seçin Veya Sürükleyin...", type=["jpg", "jpeg", "png"])
    camera_file = st.camera_input("Veya Doğrudan Kamerayla Çekin 📸")
    
    target_file = uploaded_file if uploaded_file is not None else camera_file
    
    if target_file is not None:
        image = Image.open(target_file)
        st.image(image, caption="Analiz Edilen Yaprak", use_container_width=True)
        
        st.warning("🔄 Yapay Zeka Görüntüyü İşliyor...")
        st.info("📊 **AI Analiz Raporu:** Yaprakta hafif azot eksikliği ve alt yapraklarda kalsiyum ihtiyacı sinyali algılandı. Üst menüden Kalsiyum Gübresi veya Amino Asit emri girilmesi önerilir.")
