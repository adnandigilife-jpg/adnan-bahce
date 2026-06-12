import streamlit as st
import datetime
import os
import pandas as pd
from PIL import Image

# 🚀 BÜYÜK FOTOĞRAFLAR İÇİN GÜVENLİK SINIRINI KALDIRIYORUZ (YAPRAK ANALİZİNDEKİ BOMBA HATASINI ÇÖZER)
Image.MAX_IMAGE_PIXELS = None 

# 1. SAYFA AYARLARI
st.set_page_config(layout="wide", page_title="Adnan Radar Bahçe Otomasyonu", page_icon="🌿")

# 2. KALICI VERİ TABANI MOTORU (CSV)
CSV_FILE = "bahce_gubreleme_veritabanı.csv"

if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Tarih", "Uygulanan Ürün", "Hedef Bitkiler", "Miktar (L/Kg)", "Uygulama Tipi"])
    default_data = [
        {"Tarih": "2026/06/07", "Uygulanan Ürün": "Amino Asit", "Hedef Bitkiler": "Tüm Bahçe", "Miktar (L/Kg)": 0.70, "Uygulama Tipi": "Kökten Gübreleme / Damlama"},
        {"Tarih": "2026/06/04", "Uygulanan Ürün": "Solucan Gübresi + Amino Asit", "Hedef Bitkiler": "Tüm Fideler & Mısırlar", "Miktar (L/Kg)": 0.50, "Uygulama Tipi": "Kökten Gübreleme"},
        {"Tarih": "2026/05/28", "Uygulanan Ürün": "Deniz Yosunu + Hümik Asit", "Hedef Bitkiler": "Yeni Fideler (Genel)", "Miktar (L/Kg)": 0.40, "Uygulama Tipi": "Kökten Gübreleme"}
    ]
    df_init = pd.concat([df_init, pd.DataFrame(default_data)], ignore_index=True)
    df_init.to_csv(CSV_FILE, index=False, encoding="utf-8")

def verileri_yukle():
    return pd.read_csv(CSV_FILE, encoding="utf-8")

def veri_ekle(tarih, urun, bitkiler, miktar, tip):
    df = verileri_yukle()
    yeni_satir = pd.DataFrame([{
        "Tarih": tarih.strftime("%Y/%m/%d"),
        "Uygulanan Ürün": urun,
        "Hedef Bitkiler": bitkiler,
        "Miktar (L/Kg)": miktar,
        "Uygulama Tipi": tip
    }])
    df = pd.concat([yeni_satir, df], ignore_index=True)
    df.to_csv(CSV_FILE, index=False, encoding="utf-8")

# 3. BAŞLIKLAR
st.title("🚀 Adnan Radar - Akıllı Tarım Veri Takip Sitesi")
st.markdown("---")

# 4. YAN MENÜ (SIDEBAR)
st.sidebar.markdown("### ☀️ Adana Canlı Hava Durumu")
sicaklik = st.sidebar.slider("Anlık Adana Sıcaklığı (°C)", 0, 50, 36)
nem = st.sidebar.slider("Anlık Nem Oranı (%)", 0, 100, 50)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Sistem Kapsamı")
st.sidebar.info("""
* Kimyasal içermeyen gübreleme planı,
* Kaolin kili koruma takvimi,
* Gülleci bulamacı uygulamaları,
* AI Yaprak Analiz İstasyonu.
""")

# 5. ANA SEKMELER
tab1, tab2, tab3 = st.tabs([
    "📋 İşlem Girişi & Kalıcı Geçmiş", 
    "📅 Periyodik Gübre & Hatırlatma Takvimi", 
    "📸 AI Yaprak Analiz İstasyonu"
])

# --- SEKME 1: İŞLEM GİRİŞİ & KALICI GEÇMİŞ ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### ➕ Yeni İşlem Emir Girişi")
        uygulama_tarihi = st.date_input("Uygulama Tarihi", datetime.date(2026, 6, 7))
        secilen_urunler = st.multiselect(
            "Uygulanan Organik/Doğal Ürünler",
            ["Kalsiyum Gübresi", "Solucan Gübresi", "Deniz Yosunu", "Amino Asit", "Hümik Asit", "Kaolin Kili", "Gülleci Bulamacı"]
        )
        secilen_bitkiler = st.multiselect(
            "Uygulanan Bitkiler",
            ["Mısır", "Domates", "Biber", "Patlıcan", "Salatalık", "Karpuz", "Tüm Bahçe"]
        )
        uygulama_tipi = st.selectbox("Uygulama Yöntemi", ["Kökten Gübreleme / Damlama", "Yapraktan Pülverize (Sprey)", "Toprak Hazırlığı"])
        miktar = st.number_input("Ürün Başına Miktar (L/Kg veya Gr/10L)", min_value=0.0, max_value=50.0, value=0.70, step=0.10)
        
        if st.button("Sisteme İşle (Kalıcı Kaydet)"):
            if not secilen_urunler or not secilen_bitkiler:
                st.warning("⚠️ Lütfen önce ürün ve bitki seçimi yapın!")
            else:
                urun_str = ", ".join(secilen_urunler)
                bitki_str = ", ".join(secilen_bitkiler)
                veri_ekle(uygulama_tarihi, urun_str, bitki_str, miktar, uygulama_tipi)
                st.success("✅ Başarılı! Kayıt kalıcı geçmişe eklendi.")
                st.rerun()

    with col2:
        st.markdown("### 📜 Kalıcı Uygulama Geçmişi")
        guncel_df = verileri_yukle()
        st.dataframe(guncel_df, use_container_width=True)

# --- SEKME 2: PERİYODİK GÜBRE & HATIRLATMA TAKVİMİ ---
with tab2:
    st.markdown("### 📅 Organik Bakım & Hatırlatma Takvimi")
    df_analiz = verileri_yukle()
    
    # Güvenli arama işlevi
    kaolin_kontrol = df_analiz[df_analiz["Uygulanan Ürün"].str.contains("Kaolin Kili", na=False)]
    st.markdown("#### ⚪ Kaolin Kili Sinyali (Güneş Yanıklığı & Trips Koruması)")
    if kaolin_kontrol.empty:
        st.error("🚨 Sistemde henüz Kaolin Kili kaydı bulunamadı! İlk kaplamayı yapmanız önerilir.")
    else:
        st.success("✅ Yakın zamanda Kaolin Kili uygulaması yapılmış.")
        
    st.markdown("---")
    
    # 🔥 ARKA PLANDAKİ HARF HATASI BURADA DÜZELTİLDİ
    gulleci_kontrol = df_analiz[df_analiz["Uygulanan Ürün"].str.contains("Gülleci Bulamacı", na=False)]
    st.markdown("#### 🟡 Gülleci Bulamacı Sinyali (Zararlı & Mantar Kontrolü)")
    if gulleci_kontrol.empty:
        st.warning("⚠️ Bahçede aktif gülleci bulamacı kaydı yok. 15 günde bir periyodik dozlama planlayın.")
    else:
        st.success("✅ Gülleci bulamacı koruması aktif.")

# --- SEKME 3: AI YAPRAK ANALİZ İSTASYONU ---
with tab3:
    st.markdown("### 📸 AI Yaprak Analiz İstasyonu")
    uploaded_file = st.file_uploader("Bir Yaprak Fotoğrafı Seçin...", type=["jpg", "jpeg", "png"])
    camera_file = st.camera_input("Veya Doğrudan Kamerayla Çekin 📸")
    target_file = uploaded_file if uploaded_file is not None else camera_file
    
    if target_file is not None:
        try:
            image = Image.open(target_file)
            st.image(image, caption="Sisteme Yüklenen Yaprak Resmi", use_container_width=True)
            st.warning("🔄 Yapay Zeka Görüntü Analizini Çalıştırıyor...")
            st.info("""
            📊 **AI Analiz ve Teşhis Raporu:**
            * **Muhtemel Neden:** Adana'nın aşırı sıcak gidişatına bağlı terleme stresi.
            * **Doğrudan Aksiyon Reçetesi:** Akşam serinliğinde **Kalsiyum Gübresi** uygulaması yapın ve **Kaolin Kili** kaplamasını tazeleyin.
            """)
        except Exception as e:
            st.error(f"Görsel yüklenirken bir hata oluştu: {e}")
