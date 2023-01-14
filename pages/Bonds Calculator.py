import streamlit as st
import pandas as pd
import numpy as np

page_title = "Bonds Calculator"
st.set_page_config(
    page_title=f"{page_title}",
    page_icon="💹",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

with st.sidebar:
    st.header("About")
    st.info("This web app is made by Pamella Cathryn. You can follow me on [LinkedIn](https://linkedin.com/in/pamellacathryn) | [Instagram](https://instagram.com/pamellacathryn) | [GitHub](https://github.com/pamellacathryn)")

st.markdown(f"<h1 style='text-align: center; '>{page_title}</h1>",
                unsafe_allow_html=True)
st.markdown("---")

st.subheader("Inputs:")

col1, col2 = st.columns(2)
with col1:
    i = st.number_input('Yield Rate (%)', min_value=0.01, step=0.1, value=5.00)/100
    F = st.number_input("Par Value (Face Amount)", min_value=0.00, max_value=None, value=1000.00)
    n = st.number_input("Number of Coupon Payment Periods", min_value=1, max_value=None, value=20)
with col2:
    r = st.number_input('Coupon Rate (%)', min_value=0.01, step=0.1, value=4.20)/100
    C = st.number_input("Redemption Value", min_value=0.00, max_value=None, value=1050.00)

st.write("")

letsgo = st.button("Calculate")

if letsgo:
    st.subheader("Summary")
    v = 1/(1+i)
    Fr = F*r
    g = Fr/C
    K = C*v**n
    G = Fr/i
    an = (1-v**n)/i
    P = Fr*an+K


    t = [i for i in range(n+1)]
    kupon = [0]+[round(Fr,2) for i in range(n)]
    buku = []
    imbai = [0]
    pokok = [0]
    for j in range(n+1):
        if j == 0:
            buku.append(P)
        else:
            imbai.append(i*buku[j-1])
            pokok.append(Fr-imbai[j])
            buku.append(buku[j-1]-pokok[j])
    st.markdown(
            """<style>
                .col_heading   {text-align: center !important}
            </style>
            """, unsafe_allow_html=True)


    if P - C > 0:
        text_1 = "sold at premium"
    else:
        text_1 = "sold at discount"
    kol1, kol2, kol3, kol4 = st.columns(4)
    with kol1:
        st.metric("Bond Price", f"{round(P, 2)}", text_1, delta_color="off")
    with kol2:
        st.metric("Total Coupon", f"{round(np.sum(kupon), 2)}")
    with kol3:
        st.metric("Total Interest Earned", f"{round(np.sum(imbai), 2)}")
    with kol4:
        st.metric("Total Principal Paid", f"{round(np.sum(pokok), 2)}")
    pokok = np.abs(pokok)
    st.markdown(f"<h3 style='text-align: center; '>Amortization Schedule</h3>",
                unsafe_allow_html=True)
    df = pd.DataFrame(list(zip(t, kupon, imbai, pokok, buku)),
                      columns=['Period', 'Coupon', 'Interest Earned', 'Principal Adjustment', 'Book Value'])
    st.table(df.style.format("{:.2f}"))
