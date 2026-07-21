import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Site Sakini Bilgi Sistemi", page_icon="🏢", layout="centered")

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

st.title("🏢 Green Hill City Sitesi Bilgi Güncelleme Formu")
st.markdown("Değerli komşularımız, site yönetimimizin iletişim ve araç altyapısını güncel tutabilmek için lütfen bu formu eksiksiz doldurunuz.")
st.markdown("---")

# Blok ve daire sayilari guncellendi (F1: 16 olarak ayarlandi)
blocks_config = {
    "1A": 10, "1B": 12, "1C": 3,
    "2A": 8, "2B": 8, "2C": 16, "2D": 16, "2E": 8,
    "F1": 12, "F2": 12
}

EXCEL_FILE = "site_sakinleri_veritabani.xlsx"

def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=[
            "Kayıt Tarihi", "Blok", "Daire No", "Mülk Sahibi Ad Soyad", 
            "Mülk Sahibi Tel", "Mülk Sahibi E-posta", "İkamet Durumu", 
            "Kiracı Ad Soyad", "Kiracı Tel", "Kiracı E-posta", 
            "Araç Plaka 1", "Araç Plaka 2", "Araç Plaka 3"
        ])

# --- st.form KALDIRILDI, STANDART DİNAMİK YAPI EKLENDİ ---

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
submitted = st.button("Bilgileri Kaydet")

if submitted:
    if not owner_name or not owner_phone:
        st.error("Lütfen mülk sahibinin Adı Soyadı ve Telefon numarasını eksiksiz doldurun.")
    else:
        df = load_data()
        
        new_row = {
            "Kayıt Tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Blok": selected_block,
            "Daire No": flat_number,
            "Mülk Sahibi Ad Soyad": owner_name,
            "Mülk Sahibi Tel": owner_phone,
            "Mülk Sahibi E-posta": owner_email,
            "İkamet Durumu": residence_status,
            "Kiracı Ad Soyad": tenant_name,
            "Kiracı Tel": tenant_phone,
            "Kiracı E-posta": tenant_email,
            "Araç Plaka 1": plate_1,
            "Araç Plaka 2": plate_2,
            "Araç Plaka 3": plate_3
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        
        st.markdown('<div class="success-box">✅ Bilgileriniz başarıyla kaydedildi. Teşekkür ederiz!</div>', unsafe_allow_html=True)