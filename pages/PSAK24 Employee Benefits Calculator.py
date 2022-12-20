import streamlit as st
import pandas as pd
import numpy as np
import babel.numbers
import altair as alt

page_title = "PSAK24 Employee Benefits Calculator"
st.set_page_config(
    page_title=f"{page_title}",
    page_icon=":older_adult:",
    layout="centered",
    initial_sidebar_state="collapsed",
)
with st.sidebar:
    st.header("About")
    st.info("This web app is made by Pamella Cathryn. You can follow me on [LinkedIn](https://linkedin.com/in/pamellacathryn) | [Instagram](https://instagram.com/pamellacathryn) | [GitHub](https://github.com/pamellacathryn)")

st.markdown(f"<h1 style='text-align: center; '>{page_title}</h1>",
                unsafe_allow_html=True)
st.markdown("---")

st.markdown(f'<div style="text-align: justify;"></div>', unsafe_allow_html=True)

def get_up(MK):
    if MK < 1:
        return(1)
    elif MK < 2:
        return(2)
    elif MK < 3:
        return(3)
    elif MK < 4:
        return(4)
    elif MK < 5:
        return(5)
    elif MK < 6:
        return(6)
    elif MK < 7:
        return(7)
    elif MK < 8:
        return(8)
    else:
        return(9)

def get_upmk(MK):
    if MK < 3:
        return(0)
    elif MK < 6:
        return(2)
    elif MK < 9:
        return(3)
    elif MK < 12:
        return(4)
    elif MK < 15:
        return(5)
    elif MK < 18:
        return(6)
    elif MK < 21:
        return(7)
    elif MK < 24:
        return(8)
    else:
        return(10)

def rupiah(angka):
    return babel.numbers.format_currency(str(angka), "Rp", locale='id_ID')

st.subheader("Inputs:")

based = st.selectbox("Pilih Rumus Imbalan", ["Sesuai UUCK & PP35/2021", "Custom UP & UPMK", "Imbalan Tetap"])
kols1, kols2 = st.columns(2)
sekarang = kols1.number_input("Masukkan usia saat ini", min_value=0, max_value=None, value=55)
gaji = kols2.number_input("Masukkan gaji bulanan saat ini", min_value=0, max_value=None, value=1)
masuk = kols1.number_input("Masukkan usia saat masuk kerja", min_value=0, max_value=None, value=25)
pensiun = kols2.number_input("Masukkan usia keluar kerja/pensiun yang ditetapkan", min_value=0, max_value=None, value=65)
naik = kols1.number_input("Masukkan tingkat kenaikkan gaji tahunan (%)", min_value=0.00, max_value=None, value=2.00) / 100
bunga = kols2.number_input("Masukkan tingkat suku bunga efektif tahunan (%)", min_value=0.00, max_value=None, value=4.00) / 100
MK_lalu = sekarang - masuk
MK_depan = pensiun - sekarang
MK_total = pensiun - masuk
UP = get_up(MK_total)
UPMK = get_upmk(MK_total)
if based == "Sesuai UUCK & PP35/2021":
    alasan = st.selectbox("Masukkan alasan berhenti kerja", ["Pensiun", "Cacat/Sakit Berkepanjangan", "Meninggal Dunia"])
    if alasan == "Pensiun":
        imbalan = (1.75 * UP + 1 * UPMK) * gaji * (1+naik)**(MK_depan)
    elif alasan == "Cacat/Sakit Berkepanjangan":
        imbalan = (2 * UP + 1 * UPMK) * gaji * (1+naik)**(MK_depan)
    elif alasan == "Meninggal Dunia":
        imbalan = (2 * UP + 1 * UPMK) * gaji * (1+naik)**(MK_depan)
elif based == "Custom UP & UPMK":
    st.subheader("Rumus Pengali Gaji: a x UP + b x UPMK")
    a = st.number_input("Masukkan a", min_value=0.00, max_value=None, value=1.75)
    b = st.number_input("Masukkan b", min_value=0.00, max_value=None, value=1.75)
    imbalan = (a * UP + b * UPMK) * gaji * (1+naik)**(MK_depan)
elif based == "Imbalan Tetap":
    imbalan = st.number_input("Masukkan besar imbalan tetap", min_value=0, max_value=None, value=1000)

letsgo = st.button("Calculate")

if letsgo:
    st.subheader("Summary")
    koloms1, koloms2 = st.columns(2)
    koloms1.metric("Total Imbalan", rupiah(imbalan))
    PVFB = imbalan * (1+bunga)**(-MK_depan)
    koloms2.metric("Nilai Kini Imbalan (PVFB)", rupiah(PVFB))
    unit = PVFB/MK_total
    koloms1.metric("Unit Imbalan", rupiah(unit))
    NKKIP = unit * MK_lalu
    koloms2.metric(f"NKKIP/PVDBO Usia {sekarang}", f"{rupiah(NKKIP)}")

    st.subheader("Ilustrasi")
    x_an = [i for i in range(masuk, pensiun+1)]
    data = [0 for i in range(len(x_an))]
    label = ["" for i in range(len(x_an))]
    for i in range(sekarang-masuk+1):
        data[i] = round(unit, 2)
        label[i] = "Unit"
    data[-1] = round(imbalan, 2)
    label[-1] = "Total Imbalan"
    gabung = list(zip(x_an, label, data))
    source = pd.DataFrame(gabung, columns=['Usia', 'Label', 'Value'])
    chart = alt.Chart(source).mark_bar(opacity=0.7).encode(
        x='Usia',
        y=alt.Y('Value', stack=None),
        color="Label",
    )
    st.altair_chart((chart).interactive(), use_container_width=True)
