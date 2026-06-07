import streamlit as st
import datetime
import os
import pandas as pd
from PIL import Image

# 1. SAYFA AYARLARI
st.set_page_config(layout="wide", page_title="Adnan Radar Bahçe Otomasyonu", page_icon="🌿")

# 2. KALICI VERİ TABANI MOTORU (CSV)
CSV_FILE = "bahce_gubreleme_veritabanı.csv"

# Eğer veritabanı dosyası yoksa ilk kez oluşturuyoruz
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Tarih", "Uygulanan Ürün", "Hedef Bitkiler", "Miktar (L/Kg)", "Uygulama Tipi"])
    # Varsayılan eski kayıtları ekleyelim ki boş görünmesin
    default_data = [
        {"Tarih": "2026/06/04", "Uygulanan Ürün": "Solucan Gübresi + Amino Asit", "Hedef Bitkiler": "Tüm Fideler & Mısırlar", "Miktar (L/Kg)": 0.50, "Uygulama Tipi": "Kökten Gübreleme"},
        {"Tarih": "2026/05/28", "Uygulanan Ürün": "Deniz Yosunu + Hümik Asit", "Hedef Bitkiler": "Yeni Fideler (Genel)", "Miktar (L/Kg)": 0.40, "Uygulama Tipi": "Kökten Gübreleme"}
    ]
    df_init = pd.concat([df_init, pd.DataFrame(default_data)], ignore_index=True)
    df_init.to_csv(CSV_FILE, index=False, encoding="utf-8")

# Verileri dosyadan okuma fonksiyonu
def verileri_yukle():
    return pd.read_csv(CSV_FILE, encoding="utf-8")

# Verileri dosyaya kaydetme fonksiyonu
def veri_ekle(tarih, urun, bitkiler, miktar, tip):
    df = verileri_yukle()
    yeni_satir = pd.DataFrame([{
        "Tarih": tarih.strftime("%Y/%m/%d"),
        "Uygulanan Ürün": urun,
        "Hedef Bitkiler": bitkiler,
        "Miktar (L/Kg)": miktar,
        "Uygulama Tipi": tip
    }])
    df = pd.concat([yeni_satir, df], ignore_index=True) # En yeni kaydı en üste koyar
    df.to_csv(CSV_FILE, index=False, encoding="utf-8")

# 3. BAŞLIKLAR
st.title("🚀 Adnan Radar - Akıllı Organik Tarım Analiz Veri Sitesi v3.0")
st.markdown("---")

# 4. YAN MENÜ (SIDEBAR) - HAVA DURUMU & BİLGİ PANELİ
st.sidebar.markdown("### ☀️ Adana Canlı Hava Durumu")
sicaklik = st.sidebar.slider("Anlık Adana Sıcaklığı (°C)", 0, 50, 36)
nem = st.sidebar.slider("Anlık Nem Oranı (%)", 0, 100, 50)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Sistem Kapsamı")
st.sidebar.info("""
Bu sistem Adana'daki 100m² organik hobi bahçenizin;
* Kimyasal içermeyen gübreleme planını,
* Kaolin kili koruma takvimini,
* Gülleci bulamacı uygulamalarını eksiksiz takip eder.
""")

# 5. ANA SEKMELER (TABS)
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
        st.write("Bahçede yaptığınız uygulamayı buraya girin, otomatik olarak kalıcı hafızaya kaydedilsin.")
        
        uygulama_tarihi = st.date_input("Uygulama Tarihi", datetime.date(2026, 6, 7))
        
        # Tam istediğin özel ürün listesi
        secilen_urunler = st.multiselect(
            "Uygulanan Organik/Doğal Ürünler",
            ["Kalsiyum Gübresi", "Solucan Gübresi", "Deniz Yosunu", "Amino Asit", "Hümik Asit", "Kaolin Kili", "Gülleci Bulamacı"]
        )
        
        secilen_bitkiler = st.multiselect(
            "Uygulanan Bitkiler",
            ["Mısır", "Domates", "Biber", "Patlıcan", "Salatalık", "Karpuz", "Tüm Bahçe"]
        )
        
        # Kaolin kili veya gülleci bulamacı yapraktan pülverize edilir, gübreler kökten verilebilir
        uygulama_tipi = st.selectbox("Uygulama Yöntemi", ["Kökten Gübreleme / Damlama", "Yapraktan Pülverize (Sprey)", "Toprak Hazırlığı"])
        
        miktar = st.number_input("Ürün Başına Miktar (L/Kg veya Gr/10L)", min_value=0.0, max_value=50.0, value=0.70, step=0.10)
        
        if st.button("Sisteme İşle (Kalıcı Kaydet)"):
            if not secilen_urunler or not secilen_bitkiler:
                st.warning("⚠️ Lütfen önce ürün ve bitki seçimi yapın!")
            else:
                urun_str = ", ".join(secilen_urunler)
                bitki_str = ", ".join(secilen_bitkiler)
                
                # Kalıcı CSV dosyasına yazıyoruz
                veri_ekle(uygulama_tarihi, urun_str, bitki_str, miktar, uygulama_tipi)
                st.success(f"✅ Başarılı! {urun_str} uygulaması kalıcı veri tabanına işlendi.")
                st.balloons()

    with col2:
        st.markdown("### 📜 Kalıcı Uygulama Geçmişi")
        st.write("Veri tabanından okunan, sayfa yenilense de asla silinmeyen güncel kayıtlarınız:")
        
        # Güncel verileri dosyadan okuyup ekrana basıyoruz
        guncel_df = verileri_yukle()
        st.dataframe(guncel_df, use_container_width=True)


# --- SEKME 2: PERİYODİK GÜBRE & HATIRLATMA TAKVİMİ ---
with tab2:
    st.markdown("### 📅 Organik Bakım & Hatırlatma Takvimi")
    st.write("Adana iklimi ve bitkilerinizin gelişim evrelerine göre düşüncenizi zorlamayacak periyodik hatırlatıcılar:")
    
    # Mevcut tarihe göre analiz yapıyoruz
    df_analiz = verileri_yukle()
    
    # Kaolin Kili Kontrolü
    kaolin_kontrol = df_analiz[df_analiz["Uygulanan Ürün"].str.contains("Kaolin Kili", na=False)]
    st.markdown("#### ⚪ Kaolin Kili Sinyali (Güneş Yanıklığı & Trips Koruması)")
    if kaolin_kontrol.empty:
        st.error("🚨 Sistemde henüz Kaolin Kili kaydı bulunamadı! Mısır ve domatesleri Adana sıcağından korumak için ilk kaplamayı yapmanız önerilir.")
    else:
        st.success("✅ Yakın zamanda Kaolin Kili uygulaması yapılmış. Yapraklardaki beyaz tabaka yağmurlarla veya rüzgarla aşınana kadar güvendesiniz.")
        
    st.markdown("---")
    
    # Gülleci Bulamacı Kontrolü
    gulleci_kontrol = df_analiz[df_analiz["Uygulanan Ürün"].str.contains("Gülleci Bulamacı", na=False)]
    st.markdown("#### 🟡 Gülleci Bulamacı Sinyali (Zararlı & Mantar Kontrolü)")
    if gulleci_kontrol.empty:
        st.warning("⚠️ Bahçede aktif gülleci bulamacı kaydı yok. Yaprak bitleri ve küllemeye karşı akşam serinliğinde 15 günde bir periyodik dozlama planlayın.")
    else:
        st.success("✅ Gülleci bulamacı koruması aktif.")

    st.markdown("---")
    st.markdown("#### 🗓️ Bitki Bazlı Periyodik Rutin Önerileri")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.info("**🍅 Domates & Biber & Patlıcan**\n\n* **Kalsiyum Gübresi:** Çiçek burnu çürüklüğünü önlemek için 7-10 günde bir düzenli verilmeli.\n* **Amino Asit:** Sıcak stresini kırmak için deniz yosunu ile karıştırıp yapraktan pülverize edin.")
    with col_t2:
        st.info("**🌽 Mısırlar (Hızlı Boylanma)**\n\n* **Solucan Gübresi + Hümik Asit:** Kök gelişimini ve azot alımını patlatmak için sulama suyuna karıştırın.\n* **Yabancı Ot Temizliği:** Bu evrede mısır diplerini temiz tutun.")
    with col_t3:
        st.info("**🍉 Karpuz & Salatalık**\n\n* **Deniz Yosunu:** Meyve tutumunu ve saçak kökleri teşvik etmek için periyodik olarak her 2 sulamada bir uygulayın.")


# --- SEKME 3: AI YAPRAK ANALİZ İSTASYONU ---
with tab3:
    st.markdown("### 📸 AI Yaprak Analiz İstasyonu")
    st.write("Bahçede yapraklarda bir sararma, leke veya hastalık gördüğünüzde fotoğrafını yükleyin veya çekin.")
    
    uploaded_file = st.file_uploader("Bir Yaprak Fotoğrafı Seçin...", type=["jpg", "jpeg", "png"])
    camera_file = st.camera_input("Veya Doğrudan Kamerayla Çekin 📸")
    
    target_file = uploaded_file if uploaded_file is not None else camera_file
    
    if target_file is not None:
        image = Image.open(target_file)
        st.image(image, caption="Sisteme Yüklenen Yaprak Resmi", use_container_width=True)
        
        st.warning("🔄 Yapay Zeka Görüntü Analizini Çalıştırıyor...")
        
        # Dinamik akıllı analiz simülasyonu
        st.info("""
        📊 **AI Analiz ve Teşhis Raporu:**
        * **Tespit Edilen Durum:** Alt yapraklarda damar aralarında sararma ve uçlarda kuruma başlangıcı.
        * **Muhtemel Neden:** Adana'nın aşırı sıcak gidişatına bağlı terleme stresi ve topraktan Kalsiyum / Magnezyum alımında yavaşlama.
        * **Doğrudan Aksiyon Reçetesi:** Akşam serinliğinde **Kalsiyum Gübresi** uygulaması yapın. Yaprakları korumak ve trips zararlısını uzak tutmak için **Kaolin Kili** kaplamasını tazeleyin.
        """)
