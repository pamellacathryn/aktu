import streamlit as st
import pandas as pd

page_title = "Amortization Schedule Calculator"
st.set_page_config(
    page_title=f"{page_title}",
    page_icon="📅",
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

def convert(a):
    if a == 'Monthly':
        return(1)
    elif a == 'Quarterly':
        return(3)
    elif a == 'Semi-anually':
        return(6)
    elif a == 'Anually':
        return(12)

st.subheader("Inputs:")
loan = st.number_input('Loan amount', min_value=0, value=1000)
col1, col2 = st.columns(2)
per = col1.number_input('Loan term (years)', min_value=1, value=8)
bunga = col2.number_input('Effective rate of interest (%)', min_value=0.01, step=0.1, value=8.00)
pay_period = convert(col1.selectbox(
    'Payment periods',
    ('Monthly', 'Quarterly', 'Semi-anually', 'Anually'),
    index = 3))
int_period = convert(col2.selectbox(
    'Interest conversion periods',
    ('Monthly', 'Quarterly', 'Semi-anually', 'Anually'),
    index = 3))
st.write("")

letsgo = st.button("Calculate")

if letsgo:
    st.subheader("Summary")
    interest = (1+bunga/100)**(pay_period/int_period)-1
    pay_period, int_period = 12/pay_period, 12/int_period
    n = per*pay_period
    v = 1/(1+interest)
    period = [round(n/pay_period,2) for n in range(int(n+1))]
    an = (1-v**n)/interest
    R = loan/an
    payment = [0 for i in range(len(period))]
    a = 1/pay_period
    OLB = [0 for i in range(len(period))]
    int_paid = [0 for i in range(len(period))]
    prin_paid = [0 for i in range(len(period))]
    sum = 0
    sum2 = 0
    for i in range(len(period)):
        if i == 0:
            OLB[i]=loan
        if i != 0:
            if round(period[i],2)==round(a,2):
                payment[i] = R
                int_paid[i] = interest * OLB[i - 1]
                a+=1/pay_period
            prin_paid[i]=payment[i]-int_paid[i]
            OLB[i]=OLB[i-1]-prin_paid[i]
        sum+=int_paid[i]
        sum2+=payment[i]
    OLB = [round(i,2) for i in OLB]
    OLB[-1] = abs(OLB[-1])
    col1, col2, col3 = st.columns(3)
    col1.metric("Level Payment", f"{round(R, 2)}", f"{round(100*R/loan,2)}% of Loan", delta_color="inverse")
    col2.metric("Total Interest Paid", f"{round(sum,2)}")
    col3.metric("Total Cost of Loan", f"{round(sum2,2)}", f"{round(100*sum2/loan-1,2)}% of Loan", delta_color="inverse")
    t = [i for i in range(len(period))]
    st.markdown(
        """<style>
            .col_heading   {text-align: center !important}
        </style>
        """, unsafe_allow_html=True)
    df = pd.DataFrame(list(zip(t, period, payment, int_paid, prin_paid, OLB)),
                      columns=['t','Year', 'Payment Amount', 'Interest Paid', 'Principal Repaid', 'Outstanding Loan Balance'])
    st.table(df.style.format("{:.2f}"))
