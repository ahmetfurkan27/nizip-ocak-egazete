import base64
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
ADMIN_SIFRE = "NizipOcak2026"

VARSAYILAN_VERI = {
    "sayi_tarih": "Ağustos 2026 / Sayı: 1",
    "arkaplan_logo": "",  # Genel arka plan logosu
    # SAYFA 1: MANŞET & GÜNDEM
    "manset_baslik": "ÜLKÜ OCAKLARI NİZİP İLÇE BAŞKANLIĞI FAALİYETLERİNE HIZ KESMEDEN DEVAM EDİYOR",
    "manset_altbaslik": "Nizip gençliği milli ve ahlaki şuurla geleceğe emin adımlarla hazırlanıyor.",
    "manset_icerik": (
        "Nizip İlçe Başkanlığı olarak Türk gençliğinin milli ve manevi değerlerle yetişmesi gayesiyle "
        "başlattığımız eğitim seminerleri, kültürel etkinlikler ve sosyal sorumluluk projeleri tüm hızıyla sürmektedir. "
        "Gençlerimizin yarınlara güçlü adımlarla yürümesi adına çalışmalarımız aralıksız devam edecektir."
    ),
    "manset_foto": "",
    "kose1_baslik": "Milli Şuur ve Birlik",
    "kose1_altbaslik": "Geleceğin teminatı Türk gençliğidir",
    "kose1_icerik": "Teşkilatımızın her bir neferi, milletimizin değerlerini koruma ve yaşatma azmindedir.",
    "kose1_foto": "",
    "kose2_baslik": "Eğitim ve Gençlik Çalışmaları",
    "kose2_altbaslik": "Kitap okuma ve gelişim halkaları",
    "kose2_icerik": "Gençlerimizin akademik ve ahlaki gelişimi için eğitim faaliyetlerimize aralıksız devam ediyoruz.",
    "kose2_foto": "",
    # SAYFA 2: TEŞKİLAT & İLÇE FAALİYETLERİ
    "s2_haber1_baslik": "Sosyal Sorumluluk ve Yardımlaşma Seferberliği",
    "s2_haber1_altbaslik": "İlçemizde gönüllere dokunan örnek teşkilat çalışmaları",
    "s2_haber1_icerik": "Nizip genelinde ihtiyaç sahibi vatandaşlarımıza yönelik dayanışma ve sosyal destek projelerimiz hız kesmeden devam ediyor.",
    "s2_foto1": "",
    "s2_haber2_baslik": "Haftalık İstişare ve Eğitim Buluşmaları",
    "s2_haber2_altbaslik": "Gençlerle her hafta aynı heyecanla bir aradayız",
    "s2_haber2_icerik": "Ocak binamızda her hafta düzenli olarak icra edilen seminerlerde milli kültür, tarih ve şahsiyet bilinci işlenmektedir.",
    "s2_foto2": "",
    # SAYFA 3: TARİH & KÜLTÜR KÖŞESİ
    "s3_baslik": "Köklü Maziden Güçlü Geleceğe: Türk Tarihi ve Kültürümüz",
    "s3_altbaslik": "Tarihini bilmeyen milletlerin coğrafyasını başkaları çizer",
    "s3_icerik": (
        "Türk milleti, asırlar boyunca kurduğu devletler, inşa ettiği medeniyetler ve adalet ülküsüyle tarihe yön vermiştir. "
        "Milli hafızamızı diri tutmak, ecdadımızın kutlu mirasına sahip çıkmak ve bu mirası yarınlara taşımak hepimizin vazifesidir."
    ),
    "s3_foto1": "",
    "s3_kose_baslik": "Milli Kimlik ve Kültürel Direniş",
    "s3_kose_metin": "Kültürüne yabancılaşan toplumlar milli reflekslerini kaybederler. Milli şuur, bağımsızlığımızın teminatıdır.",
    "s3_foto2": "",
    # SAYFA 4: ŞAHSİYETLERİMİZ & TÜRK MİTOLOJİSİ & DUYURULAR
    "s4_sahsiyet_baslik": "ŞAHSİYETLERİMİZ: Bilge Kağan'dan Günümüze",
    "s4_sahsiyet_icerik": (
        "Türk milletine ömrünü adayan, 'Türk milleti için gece uyumadım, gündüz oturmadım' diyerek milleti bir araya toplayan "
        "kutlu liderlerimiz ve fikir adamlarımız yolumuzu aydınlatmaya devam ediyor."
    ),
    "s4_sahsiyet_foto": "",
    "s4_mitoloji_baslik": "TÜRK MİTOLOJİSİ: Umay Ana ve Kut Anlayışı",
    "s4_mitoloji_icerik": (
        "Eski Türk inancında ve destanlarımızda yer alan Umay Ana, bereketi ve çocukları koruyan kutlu bir simgedir. "
        "Gök Tanrı inancında devlet yönetme meşruiyetini ifade eden 'Kut' kavramı ise Türk töresinin en önemli esasıdır."
    ),
    "s4_mitoloji_foto": "",
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


# --- ÖZEL ARKA PLAN VE LOGO / FİLİGRAN CSS ENJEKSİYONU ---
def arkaplan_ayarla(logo_yolu):
    bg_css = """
    <style>
    .stApp {
        background-color: #1a1c1e;
        color: #f1f2f6;
    }
    """
    if logo_yolu and os.path.exists(logo_yolu):
        with open(logo_yolu, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read()).decode()
        bg_css = f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(20, 22, 25, 0.92), rgba(20, 22, 25, 0.92)), 
                        url("data:image/png;base64,{b64_string}");
            background-size: 550px auto;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #f1f2f6;
        }}
        </style>
        """
    st.markdown(bg_css, unsafe_allow_html=True)


arkaplan_ayarla(veri.get("arkaplan_logo", ""))

# Sol Menü
st.sidebar.title("🇹🇷 E-Gazete Menü")
sayfa_secimi = st.sidebar.radio(
    "Sayfa Seçiniz:",
    [
        "📰 Sayfa 1: Manşet & Gündem",
        "📰 Sayfa 2: Teşkilat & Faaliyetler",
        "📰 Sayfa 3: Tarih & Kültür Köşesi",
        "📰 Sayfa 4: Şahsiyetlerimiz & Mitoloji",
    ],
)

st.sidebar.markdown("---")
admin_giris = st.sidebar.checkbox("⚙️ Yönetim Paneli (Canlı Düzenle)")

# ----------------- ADMIN PANELİ -----------------
if admin_giris:
    sifre = st.sidebar.text_input("Yönetici Şifresi:", type="password")
    if sifre == ADMIN_SIFRE:
        st.sidebar.success("Yönetici girişi aktif!")
        st.header("⚙️ Canlı Gazete ve Görsel Yönetim Masası")

        with st.form("admin_form_full"):
            st.subheader("1. Genel Tasarım & Arka Plan Logosu")
            sayi_tarih = st.text_input(
                "Sayı ve Tarih:", value=veri.get("sayi_tarih", "")
            )

            bg_logo_dosya = st.file_uploader(
                "Gazete Arka Plan Logosu / Filigran Seç (PNG/JPG)",
                type=["png", "jpg", "jpeg"],
                key="bg_logo",
            )
            if bg_logo_dosya:
                with open("arkaplan_logo.png", "wb") as f:
                    f.write(bg_logo_dosya.getbuffer())
                veri["arkaplan_logo"] = "arkaplan_logo.png"

            # SAYFA 1
            st.markdown("---")
            st.markdown("### 📰 SAYFA 1: MANŞET & KÖŞELER")
            m_baslik = st.text_input(
                "Manşet Başlığı:", value=veri.get("manset_baslik", "")
            )
            m_altbaslik = st.text_input(
                "Manşet Alt Başlığı:", value=veri.get("manset_altbaslik", "")
            )
            m_icerik = st.text_area(
                "Manşet Metni:", value=veri.get("manset_icerik", ""), height=90
            )

            m_foto_dosya = st.file_uploader(
                "Manşet Fotoğrafı", type=["jpg", "png", "jpeg"], key="f_m"
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
                    height=70,
                )
                k1_f_dosya = st.file_uploader(
                    "Sol Köşe Görseli", type=["jpg", "png"], key="f_k1"
                )
                if k1_f_dosya:
                    with open("kose1_foto.jpg", "wb") as f:
                        f.write(k1_f_dosya.getbuffer())
                    veri["kose1_foto"] = "kose1_foto.jpg"

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
                    height=70,
                )
                k2_f_dosya = st.file_uploader(
                    "Sağ Köşe Görseli", type=["jpg", "png"], key="f_k2"
                )
                if k2_f_dosya:
                    with open("kose2_foto.jpg", "wb") as f:
                        f.write(k2_f_dosya.getbuffer())
                    veri["kose2_foto"] = "kose2_foto.jpg"

            # SAYFA 2
            st.markdown("---")
            st.markdown("### 📰 SAYFA 2: TEŞKİLAT VE FAALİYETLER")
            s2_1_b = st.text_input(
                "1. Faaliyet Başlığı:", value=veri.get("s2_haber1_baslik", "")
            )
            s2_1_ab = st.text_input(
                "1. Faaliyet Alt Başlığı:",
                value=veri.get("s2_haber1_altbaslik", ""),
            )
            s2_1_i = st.text_area(
                "1. Faaliyet Metni:",
                value=veri.get("s2_haber1_icerik", ""),
                height=80,
            )
            s2_f1_dosya = st.file_uploader(
                "1. Faaliyet Fotoğrafı", type=["jpg", "png"], key="f_s2_1"
            )
            if s2_f1_dosya:
                with open("s2_foto1.jpg", "wb") as f:
                    f.write(s2_f1_dosya.getbuffer())
                veri["s2_foto1"] = "s2_foto1.jpg"

            s2_2_b = st.text_input(
                "2. Faaliyet Başlığı:", value=veri.get("s2_haber2_baslik", "")
            )
            s2_2_ab = st.text_input(
                "2. Faaliyet Alt Başlığı:",
                value=veri.get("s2_haber2_altbaslik", ""),
            )
            s2_2_i = st.text_area(
                "2. Faaliyet Metni:",
                value=veri.get("s2_haber2_icerik", ""),
                height=80,
            )
            s2_f2_dosya = st.file_uploader(
                "2. Faaliyet Fotoğrafı", type=["jpg", "png"], key="f_s2_2"
            )
            if s2_f2_dosya:
                with open("s2_foto2.jpg", "wb") as f:
                    f.write(s2_f2_dosya.getbuffer())
                veri["s2_foto2"] = "s2_foto2.jpg"

            # SAYFA 3
            st.markdown("---")
            st.markdown("### 📰 SAYFA 3: TARİH VE KÜLTÜR KÖŞESİ")
            s3_b = st.text_input(
                "Tarih Başlığı:", value=veri.get("s3_baslik", "")
            )
            s3_ab = st.text_input(
                "Tarih Alt Başlığı:", value=veri.get("s3_altbaslik", "")
            )
            s3_i = st.text_area(
                "Tarih Metni:", value=veri.get("s3_icerik", ""), height=90
            )
            s3_f1_dosya = st.file_uploader(
                "Tarih Sayfası Ana Görseli", type=["jpg", "png"], key="f_s3_1"
            )
            if s3_f1_dosya:
                with open("s3_foto1.jpg", "wb") as f:
                    f.write(s3_f1_dosya.getbuffer())
                veri["s3_foto1"] = "s3_foto1.jpg"

            s3_k_b = st.text_input(
                "Tarih Köşe Başlığı:", value=veri.get("s3_kose_baslik", "")
            )
            s3_k_m = st.text_area(
                "Tarih Köşe Metni:",
                value=veri.get("s3_kose_metin", ""),
                height=70,
            )
            s3_f2_dosya = st.file_uploader(
                "Tarih Köşe Görseli", type=["jpg", "png"], key="f_s3_2"
            )
            if s3_f2_dosya:
                with open("s3_foto2.jpg", "wb") as f:
                    f.write(s3_f2_dosya.getbuffer())
                veri["s3_foto2"] = "s3_foto2.jpg"

            # SAYFA 4
            st.markdown("---")
            st.markdown(
                "### 📰 SAYFA 4: ŞAHSİYETLERİMİZ & MİTOLOJİ & DUYURULAR"
            )
            s4_s_b = st.text_input(
                "Şahsiyetlerimiz Başlığı:",
                value=veri.get("s4_sahsiyet_baslik", ""),
            )
            s4_s_i = st.text_area(
                "Şahsiyetlerimiz Metni:",
                value=veri.get("s4_sahsiyet_icerik", ""),
                height=80,
            )
            s4_sf_dosya = st.file_uploader(
                "Şahsiyetlerimiz Görseli", type=["jpg", "png"], key="f_s4_1"
            )
            if s4_sf_dosya:
                with open("s4_sahsiyet_foto.jpg", "wb") as f:
                    f.write(s4_sf_dosya.getbuffer())
                veri["s4_sahsiyet_foto"] = "s4_sahsiyet_foto.jpg"

            s4_m_b = st.text_input(
                "Türk Mitolojisi Başlığı:",
                value=veri.get("s4_mitoloji_baslik", ""),
            )
            s4_m_i = st.text_area(
                "Türk Mitolojisi Metni:",
                value=veri.get("s4_mitoloji_icerik", ""),
                height=80,
            )
            s4_mf_dosya = st.file_uploader(
                "Türk Mitolojisi Görseli", type=["jpg", "png"], key="f_s4_2"
            )
            if s4_mf_dosya:
                with open("s4_mitoloji_foto.jpg", "wb") as f:
                    f.write(s4_mf_dosya.getbuffer())
                veri["s4_mitoloji_foto"] = "s4_mitoloji_foto.jpg"

            duyurular = st.text_area(
                "Duyurular:", value=veri.get("duyurular", ""), height=80
            )

            kaydet = st.form_submit_button("💾 TÜM DEĞİŞİKLİKLERİ CANLI YAYINLA")
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
                veri["s2_haber1_baslik"] = s2_1_b
                veri["s2_haber1_altbaslik"] = s2_1_ab
                veri["s2_haber1_icerik"] = s2_1_i
                veri["s2_haber2_baslik"] = s2_2_b
                veri["s2_haber2_altbaslik"] = s2_2_ab
                veri["s2_haber2_icerik"] = s2_2_i
                veri["s3_baslik"] = s3_b
                veri["s3_altbaslik"] = s3_ab
                veri["s3_icerik"] = s3_i
                veri["s3_kose_baslik"] = s3_k_b
                veri["s3_kose_metin"] = s3_k_m
                veri["s4_sahsiyet_baslik"] = s4_s_b
                veri["s4_sahsiyet_icerik"] = s4_s_i
                veri["s4_mitoloji_baslik"] = s4_m_b
                veri["s4_mitoloji_icerik"] = s4_m_i
                veri["duyurular"] = duyurular

                veri_kaydet(veri)
                st.success(
                    "Tüm gazete içeriği ve fotoğraflar güncellendi, canlıya aktarıldı!"
                )
                st.rerun()
    elif sifre:
        st.sidebar.error("Hatalı şifre!")

# ----------------- GAZETE OKUMA SAYFALARI -----------------
st.markdown(
    f"<p style='text-align: right; color: #a4b0be;'><b>{veri['sayi_tarih']}</b> | Ülkü Ocakları Nizip İlçe Başkanlığı</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align: center; color: #3b8ed0; border-bottom: 2px solid #3b8ed0; padding-bottom: 10px;'>NİZİP OCAK BÜLTENİ</h1>",
    unsafe_allow_html=True,
)

# SAYFA 1
if sayfa_secimi == "📰 Sayfa 1: Manşet & Gündem":
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
    with col_txt:
        st.write(veri["manset_icerik"])

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {veri['kose1_baslik']}")
        st.caption(veri["kose1_altbaslik"])
        if veri.get("kose1_foto") and os.path.exists(veri["kose1_foto"]):
            st.image(veri["kose1_foto"], use_container_width=True)
        st.write(veri["kose1_icerik"])
    with col2:
        st.markdown(f"### {veri['kose2_baslik']}")
        st.caption(veri["kose2_altbaslik"])
        if veri.get("kose2_foto") and os.path.exists(veri["kose2_foto"]):
            st.image(veri["kose2_foto"], use_container_width=True)
        st.write(veri["kose2_icerik"])

# SAYFA 2
elif sayfa_secimi == "📰 Sayfa 2: Teşkilat & Faaliyetler":
    st.markdown(f"## {veri['s2_haber1_baslik']}")
    st.markdown(
        f"<p style='color: #2ecc71; font-style: italic;'>{veri['s2_haber1_altbaslik']}</p>",
        unsafe_allow_html=True,
    )

    col_img2, col_txt2 = st.columns([1.2, 2])
    with col_img2:
        if veri.get("s2_foto1") and os.path.exists(veri["s2_foto1"]):
            st.image(veri["s2_foto1"], use_container_width=True)
    with col_txt2:
        st.write(veri["s2_haber1_icerik"])

    st.markdown("---")
    st.markdown(f"### {veri['s2_haber2_baslik']}")
    st.caption(veri["s2_haber2_altbaslik"])

    col_img2_2, col_txt2_2 = st.columns([1.2, 2])
    with col_img2_2:
        if veri.get("s2_foto2") and os.path.exists(veri["s2_foto2"]):
            st.image(veri["s2_foto2"], use_container_width=True)
    with col_txt2_2:
        st.write(veri["s2_haber2_icerik"])

# SAYFA 3
elif sayfa_secimi == "📰 Sayfa 3: Tarih & Kültür Köşesi":
    st.markdown(f"## 🏛️ {veri['s3_baslik']}")
    st.markdown(
        f"<p style='color: #e67e22; font-style: italic;'>{veri['s3_altbaslik']}</p>",
        unsafe_allow_html=True,
    )

    col_img3, col_txt3 = st.columns([1.2, 2])
    with col_img3:
        if veri.get("s3_foto1") and os.path.exists(veri["s3_foto1"]):
            st.image(veri["s3_foto1"], use_container_width=True)
    with col_txt3:
        st.write(veri["s3_icerik"])

    st.markdown("---")
    st.markdown(f"### ✒️ {veri['s3_kose_baslik']}")
    if veri.get("s3_foto2") and os.path.exists(veri["s3_foto2"]):
        st.image(veri["s3_foto2"], width=350)
    st.write(veri["s3_kose_metin"])

# SAYFA 4
elif sayfa_secimi == "📰 Sayfa 4: Şahsiyetlerimiz & Mitoloji":
    st.markdown("## 🏹 Şahsiyetlerimiz ve Türk Mitolojisi")

    col_sahsiyet, col_mitoloji = st.columns(2)

    with col_sahsiyet:
        st.markdown(f"### 🐺 {veri['s4_sahsiyet_baslik']}")
        if veri.get("s4_sahsiyet_foto") and os.path.exists(
            veri["s4_sahsiyet_foto"]
        ):
            st.image(veri["s4_sahsiyet_foto"], use_container_width=True)
        st.write(veri["s4_sahsiyet_icerik"])

    with col_mitoloji:
        st.markdown(f"### 🦅 {veri['s4_mitoloji_baslik']}")
        if veri.get("s4_mitoloji_foto") and os.path.exists(
            veri["s4_mitoloji_foto"]
        ):
            st.image(veri["s4_mitoloji_foto"], use_container_width=True)
        st.write(veri["s4_mitoloji_icerik"])

    st.markdown("---")
    st.markdown("### 📢 TEŞKİLAT VE EĞİTİM DUYURULARI")
    st.info(veri["duyurular"])
