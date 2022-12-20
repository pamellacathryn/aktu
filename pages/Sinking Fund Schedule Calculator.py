import streamlit as st
import pandas as pd

page_title = "Sinking Fund Schedule Calculator"
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
col1, col2 = st.columns(2)
loan = col1.number_input('Loan amount', min_value=0, value=1000)
per = col2.number_input('Loan term (years)', min_value=1, value=4)
bunga = col1.number_input('Effective rate of interest (%)', min_value=0.01, step=0.1, value=8.00)
pay_period = convert(col1.selectbox(
    'Deposit periods',
    ('Monthly', 'Quarterly', 'Semi-anually', 'Anually'),
    index = 3))
bunga_sf = col2.number_input('Sinking Fund Effective rate of interest (%)', min_value=0.01, step=0.1, value=8.00)
int_period = convert(col2.selectbox(
    'Interest conversion periods',
    ('Monthly', 'Quarterly', 'Semi-anually', 'Anually'),
    index = 3))
st.write("")

letsgo = st.button("Calculate")

if letsgo:
    st.subheader("Summary")

    interest = (1+bunga/100)**(pay_period/int_period)-1
    i_paid = interest*loan
    pay_period, int_period = 12/pay_period, 12/int_period
    n = per*pay_period
    v = 1/(1+interest)
    period = [round(n/pay_period,2) for n in range(int(n+1))]
    an = (1-v**n)/interest
    sn = an*(1+interest)**n
    depo = loan/sn

    a = 1/pay_period
    int_paid = [0 for i in range(len(period))]
    sf_depo = [0 for i in range(len(period))]
    sf_int = [0 for i in range(len(period))]
    sf_amount = [0 for i in range(len(period))]
    OLB = [0 for i in range(len(period))]
    sum = 0
    # sum2 = 0
    for i in range(len(period)):
        if i == 0:
            OLB[i]=loan
        if i != 0:
            if round(period[i],2)==round(a,2):
                sf_depo[i] = depo
                int_paid[i] = i_paid
                a+=1/pay_period
            sf_int[i] = interest*sf_amount[i-1]
            sf_amount[i]=sf_amount[i-1]+sf_depo[i]+sf_int[i]
            OLB[i]=loan-sf_amount[i]
        sum += sf_depo[i]
        # sum2+=payment[i]
    OLB = [round(i,2) for i in OLB]
    OLB[-1] = abs(OLB[-1])
    col1, col2, col3 = st.columns(3)
    col1.metric("Sinking Fund Deposit", f"{round(depo, 2)}", f"{round(100*depo/loan,2)}% of Loan", delta_color="inverse")
    col2.metric("Total Deposit Paid", f"{round(sum,2)}", f"{round(100*sum/loan,2)}% of Loan", delta_color="inverse")
    col3.metric("Total Money Saved", f"{round(loan-sum,2)}", f"{round(abs(loan-sum)/loan-1,2)}% of Loan")
    t = [i for i in range(len(period))]
    st.markdown(
        """<style>
            .col_heading   {text-align: center !important}
        </style>
        """, unsafe_allow_html=True)
    df = pd.DataFrame(list(zip(t, period, int_paid, sf_depo, sf_int, sf_amount, OLB)),
                      columns = ['t', 'Year', 'Interest Paid', 'Sinking Fund Deposit', 'Interest Earned on Sinking Fund Deposit', 'Amount in Sinking Fund', 'Net Amount of Loan'])
    st.table(df.style.format("{:.2f}"))
