import json
import os
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Ülkü Ocakları Nizip İlçe Başkanlığı - E-Gazete",
    page_icon="🇹🇷",
    layout="wide",
)

DATA_FILE = "gazete_verileri.json"
ADMIN_SIFRE = "NizipOcak2026"  # Yönetim paneli şifreniz

VARSAYILAN_VERI = {
    "sayi_tarih": "Ağustos 2026 / Sayı: 1",
    "manset_baslik": "ÜLKÜ OCAKLARI NİZİP İLÇE BAŞKANLIĞI FAALİYETLERİNE DEVAM EDİYOR",
    "manset_altbaslik": "Nizip gençliği milli ve ahlaki şuurla geleceğe emin adımlarla hazırlanıyor.",
    "manset_icerik": (
        "Nizip İlçe Başkanlığı olarak Türk gençliğinin milli ve manevi değerlerle yetişmesi gayesiyle "
        "başlattığımız eğitim seminerleri, kültürel etkinlikler ve sosyal sorumluluk projeleri tüm hızıyla sürmektedir. "
        "Gençlerimizin yarınlara güçlü adımlarla yürümesi adına çalışmalarımız aralıksız devam edecektir."
    ),
    "manset_foto": "",
    "kose1_baslik": "Tarih ve Kültür Köşesi",
    "kose1_altbaslik": "Köklü geçmiş, aydınlık gelecek",
    "kose1_icerik": "Milli şuur, milletimizin geçmişten devraldığı en büyük mirastır. Genç nesillere tarihimizi doğru aktarmak temel görevimizdir.",
    "kose2_baslik": "Gençlik ve Eğitim",
    "kose2_altbaslik": "Kitap okuma halkaları ve etütler",
    "kose2_icerik": "Ocak bünyesinde düzenlenen kitap okuma halkaları ve ders etütleri ile Nizip gençliğini yarınlara hazırlıyoruz.",
    "s2_haber1_baslik": "Sosyal Sorumluluk ve Dayanışma Faaliyetleri",
    "s2_haber1_altbaslik": "İlçemizde gönüllere dokunan örnek çalışmalar",
    "s2_haber1_icerik": "İlçe genelinde ihtiyaç sahibi vatandaşlarımıza yönelik yardımlaşma ve dayanışma faaliyetlerimiz teşkilatımızın öncülüğünde sürmektedir.",
    "s2_foto": "",
    "duyurular": (
        "• Her Perşembe Saat 19.00'da Gençlik Sohbeti ve Eğitim Semineri.\n"
        "• Hafta sonu ücretsiz kütüphane ve ders çalışma saatleri.\n"
        "• Türk Dünyası Kültür Yarışması başvuruları başlamıştır."
    ),
}


def veri_yukle():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                v = json.load(f)
                for key, val in VARSAYILAN_VERI.items():
                    if key not in v:
                        v[key] = val
                return v
        except Exception:
            return VARSAYILAN_VERI.copy()
    return VARSAYILAN_VERI.copy()


def veri_kaydet(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


veri = veri_yukle()

# Sol Menü / Gezinme ve Admin Girişi
st.sidebar.title("🇹🇷 E-Gazete Menü")
sayfa_secimi = st.sidebar.radio(
    "Görüntüle:",
    ["📰 Sayfa 1: Manşet & Köşeler", "📰 Sayfa 2: Faaliyetler & Duyurular"],
)

st.sidebar.markdown("---")
admin_giris = st.sidebar.checkbox("⚙️ Yönetim Paneli (Canlı Düzenle)")

# ----------------- ADMIN PANELİ -----------------
if admin_giris:
    sifre = st.sidebar.text_input("Yönetici Şifresi:", type="password")
    if sifre == ADMIN_SIFRE:
        st.sidebar.success("Yönetici girişi başarılı!")
        st.header("⚙️ Canlı Gazete Düzenleme Masası")

        with st.form("admin_form"):
            st.subheader("Genel Bilgiler")
            sayi_tarih = st.text_input(
                "Sayı ve Tarih:", value=veri.get("sayi_tarih", "")
            )

            st.subheader("Sayfa 1: Manşet & Köşeler")
            m_baslik = st.text_input(
                "Manşet Başlığı:", value=veri.get("manset_baslik", "")
            )
            m_altbaslik = st.text_input(
                "Manşet Alt Başlığı:", value=veri.get("manset_altbaslik", "")
            )
            m_icerik = st.text_area(
                "Manşet Metni:", value=veri.get("manset_icerik", ""), height=120
            )

            m_foto_dosya = st.file_uploader(
                "Manşet Fotoğrafı Yükle (JPG/PNG)",
                type=["jpg", "jpeg", "png"],
                key="foto1",
            )
            if m_foto_dosya:
                with open("manset_foto.jpg", "wb") as f:
                    f.write(m_foto_dosya.getbuffer())
                veri["manset_foto"] = "manset_foto.jpg"

            col_k1, col_k2 = st.columns(2)
            with col_k1:
                k1_b = st.text_input(
                    "Sol Köşe Başlığı:", value=veri.get("kose1_baslik", "")
                )
                k1_ab = st.text_input(
                    "Sol Köşe Alt Başlığı:",
                    value=veri.get("kose1_altbaslik", ""),
                )
                k1_i = st.text_area(
                    "Sol Köşe Metni:",
                    value=veri.get("kose1_icerik", ""),
                    height=100,
                )
            with col_k2:
                k2_b = st.text_input(
                    "Sağ Köşe Başlığı:", value=veri.get("kose2_baslik", "")
                )
                k2_ab = st.text_input(
                    "Sağ Köşe Alt Başlığı:",
                    value=veri.get("kose2_altbaslik", ""),
                )
                k2_i = st.text_area(
                    "Sağ Köşe Metni:",
                    value=veri.get("kose2_icerik", ""),
                    height=100,
                )

            st.subheader("Sayfa 2: Faaliyetler & Duyurular")
            s2_b = st.text_input(
                "Sayfa 2 Başlığı:", value=veri.get("s2_haber1_baslik", "")
            )
            s2_ab = st.text_input(
                "Sayfa 2 Alt Başlığı:",
                value=veri.get("s2_haber1_altbaslik", ""),
            )
            s2_i = st.text_area(
                "Sayfa 2 Metni:",
                value=veri.get("s2_haber1_icerik", ""),
                height=120,
            )

            s2_foto_dosya = st.file_uploader(
                "Sayfa 2 Fotoğrafı Yükle (JPG/PNG)",
                type=["jpg", "jpeg", "png"],
                key="foto2",
            )
            if s2_foto_dosya:
                with open("s2_foto.jpg", "wb") as f:
                    f.write(s2_foto_dosya.getbuffer())
                veri["s2_foto"] = "s2_foto.jpg"

            duyurular = st.text_area(
                "Duyurular Listesi:",
                value=veri.get("duyurular", ""),
                height=100,
            )

            kaydet = st.form_submit_button("💾 Canlı Olarak Yayınla ve Kaydet")
            if kaydet:
                veri["sayi_tarih"] = sayi_tarih
                veri["manset_baslik"] = m_baslik
                veri["manset_altbaslik"] = m_altbaslik
                veri["manset_icerik"] = m_icerik
                veri["kose1_baslik"] = k1_b
                veri["kose1_altbaslik"] = k1_ab
                veri["kose1_icerik"] = k1_i
                veri["kose2_baslik"] = k2_b
                veri["kose2_altbaslik"] = k2_ab
                veri["kose2_icerik"] = k2_i
                veri["s2_haber1_baslik"] = s2_b
                veri["s2_haber1_altbaslik"] = s2_ab
                veri["s2_haber1_icerik"] = s2_i
                veri["duyurular"] = duyurular

                veri_kaydet(veri)
                st.success(
                    "Gazete güncellendi! Tüm ziyaretçiler anında yeni içeriği görecek."
                )
                st.rerun()
    elif sifre:
        st.sidebar.error("Hatalı şifre!")

# ----------------- KULLANICI GAZETE EKRANI -----------------
st.markdown(
    f"<p style='text-align: right; color: gray;'><b>{veri['sayi_tarih']}</b> | Ülkü Ocakları Nizip İlçe Başkanlığı</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align: center; color: #3b8ed0; border-bottom: 2px solid #3b8ed0; padding-bottom: 10px;'>NİZİP OCAK BÜLTENİ</h1>",
    unsafe_allow_html=True,
)

if sayfa_secimi == "📰 Sayfa 1: Manşet & Köşeler":
    st.markdown("### 📌 GÜNÜN MANŞETİ")
    st.markdown(f"## {veri['manset_baslik']}")
    st.markdown(
        f"<p style='color: #3498db; font-style: italic;'>{veri['manset_altbaslik']}</p>",
        unsafe_allow_html=True,
    )

    col_img, col_txt = st.columns([1.2, 2])
    with col_img:
        if veri.get("manset_foto") and os.path.exists(veri["manset_foto"]):
            st.image(veri["manset_foto"], use_container_width=True)
        else:
            st.info("Manşet görseli eklenmedi.")
    with col_txt:
        st.write(veri["manset_icerik"])

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {veri['kose1_baslik']}")
        st.caption(veri["kose1_altbaslik"])
        st.write(veri["kose1_icerik"])
    with col2:
        st.markdown(f"### {veri['kose2_baslik']}")
        st.caption(veri["kose2_altbaslik"])
        st.write(veri["kose2_icerik"])

elif sayfa_secimi == "📰 Sayfa 2: Faaliyetler & Duyurular":
    st.markdown(f"## {veri['s2_haber1_baslik']}")
    st.markdown(
        f"<p style='color: #2ecc71; font-style: italic;'>{veri['s2_haber1_altbaslik']}</p>",
        unsafe_allow_html=True,
    )

    col_img2, col_txt2 = st.columns([1.2, 2])
    with col_img2:
        if veri.get("s2_foto") and os.path.exists(veri["s2_foto"]):
            st.image(veri["s2_foto"], use_container_width=True)
        else:
            st.info("Haber görseli eklenmedi.")
    with col_txt2:
        st.write(veri["s2_haber1_icerik"])

    st.markdown("---")
    st.markdown("### 📢 TEŞKİLAT VE EĞİTİM DUYURULARI")
    st.info(veri["duyurular"])