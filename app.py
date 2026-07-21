import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Site Sakini Bilgi Sistemi", page_icon="logo.png", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        background-color: #2c3e50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
    }
    .stButton>button:hover { background-color: #34495e; color: white; }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        text-align: center;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 7])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.title("Green Hill City Sitesi Bilgi Güncelleme Formu")

st.markdown("Değerli komşularımız, site yönetimimizin iletişim ve araç bilgisini güncel tutabilmek için lütfen bu formu eksiksiz doldurunuz. Birden fazla dairesi olan kişiler her dairesi için ayrı ayrı yapmalıdır.")
st.markdown("---")

blocks_config = {
    "1A": 10, "1B": 12, "1C": 3,
    "2A": 8, "2B": 8, "2C": 16, "2D": 16, "2E": 8,
    "F1": 12, "F2": 12
}

def get_google_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    s_creds = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(s_creds, scopes=scopes)
    client = gspread.authorize(creds)
    sheet_url = st.secrets["gsheets"]["url"]
    return client.open_by_url(sheet_url).sheet1

st.subheader("1. Konum Bilgileri")
col1, col2 = st.columns(2)
with col1:
    selected_block = st.selectbox("Blok Seçiniz", list(blocks_config.keys()))
with col2:
    max_flat = blocks_config[selected_block]
    flat_number = st.selectbox("Daire Numarası", [str(i) for i in range(1, max_flat + 1)])

st.subheader("2. Mülk Sahibi Bilgileri")
owner_name = st.text_input("Mülk Sahibi Adı Soyadı")
col3, col4 = st.columns(2)
with col3:
    owner_phone = st.text_input("Mülk Sahibi Cep Telefonu (05XX...)")
with col4:
    owner_email = st.text_input("Mülk Sahibi E-posta Adresi (İsteğe bağlı)")

st.subheader("3. İkamet Durumu")
residence_status = st.radio(
    "Bu dairede kim oturuyor?",
    ["Mülk sahibi kendisi oturuyor", "Kiracı oturuyor", "Daire boş / Kapalı"]
)

tenant_name = ""
tenant_phone = ""
tenant_email = ""

if residence_status == "Kiracı oturuyor":
    st.markdown("#### Kiracı Bilgileri")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        tenant_name = st.text_input("Kiracı Adı Soyadı")
    with t_col2:
        tenant_phone = st.text_input("Kiracı Cep Telefonu (05XX...)")
    tenant_email = st.text_input("Kiracı E-posta Adresi (İsteğe bağlı)")

st.subheader("4. Araç Bilgileri (Plakalar)")
v_col1, v_col2, v_col3 = st.columns(3)
with v_col1:
    plate_1 = st.text_input("Araç Plakası 1").upper()
with v_col2:
    plate_2 = st.text_input("Araç Plakası 2").upper()
with v_col3:
    plate_3 = st.text_input("Araç Plakası 3").upper()

st.markdown("<br>", unsafe_allow_html=True)

# KVKK Onay Kutusu (Zorunlu Alan)
kvkk_onay = st.checkbox("Kişisel verilerimin site yönetimi tarafından iletişim ve güvenlik amacıyla kayıt altına alınmasını onaylıyorum.")

# Buton KVKK onayına kilitlendi (Kutucuk işaretlenmezse buton tıklanamaz)
submitted = st.button("Bilgileri Kaydet", disabled=not kvkk_onay)

if submitted:
    # Boş alan kontrolü
    if not owner_name or not owner_phone:
        st.error("Lütfen mülk sahibinin Adı Soyadı ve Telefon numarasını eksiksiz doldurun.")
    # Telefon numarası uzunluk kontrolü (Basit doğrulama)
    elif len(owner_phone.replace(" ", "")) < 10:
        st.error("Lütfen geçerli bir telefon numarası giriniz (Örn: 05XX XXX XX XX).")
    else:
        try:
            sheet = get_google_sheet()
            
            if not sheet.row_values(1):
                headers = [
                    "Kayıt Tarihi", "Blok", "Daire No", "Mülk Sahibi Ad Soyad", 
                    "Mülk Sahibi Tel", "Mülk Sahibi E-posta", "İkamet Durumu", 
                    "Kiracı Ad Soyad", "Kiracı Tel", "Kiracı E-posta", 
                    "Araç Plaka 1", "Araç Plaka 2", "Araç Plaka 3"
                ]
                sheet.append_row(headers)
            
            # Plakaları standart formata sokma (Boşlukları silme ve büyük harf yapma)
            std_plate_1 = plate_1.replace(" ", "").upper()
            std_plate_2 = plate_2.replace(" ", "").upper()
            std_plate_3 = plate_3.replace(" ", "").upper()
            
            new_row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                selected_block,
                flat_number,
                owner_name,
                owner_phone,
                owner_email,
                residence_status,
                tenant_name,
                tenant_phone,
                tenant_email,
                std_plate_1,
                std_plate_2,
                std_plate_3
            ]
            sheet.append_row(new_row)
            st.markdown('<div class="success-box">✅ Bilgileriniz başarıyla kaydedildi. Teşekkür ederiz!</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Sistemsel bir bağlantı hatası oluştu: {e}")