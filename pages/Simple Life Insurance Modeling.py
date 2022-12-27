import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

page_title = "Simple Life Insurance Modeling"
st.set_page_config(
    page_title=f"{page_title}",
    page_icon="💶",
    layout="centered",
    initial_sidebar_state="collapsed",
)
with st.sidebar:
    st.header("About")
    st.info("This web app is made by Pamella Cathryn. You can follow me on [LinkedIn](https://linkedin.com/in/pamellacathryn) | [Instagram](https://instagram.com/pamellacathryn) | [GitHub](https://github.com/pamellacathryn)")

st.markdown(f"<h1 style='text-align: center; '>{page_title}</h1>",
                unsafe_allow_html=True)

st.markdown("---")

def num_in_force(t):
    if t == 0:
        return 1
    elif t >= T:
        return 0
    else:
        return num_in_force(t-1) - num_deaths(t-1) - num_lapses(t-1)
def num_deaths(t):
    if t < T:
        return num_in_force(t) * q[t]
    else:
        return 0
def num_lapses(t):
    if t < T:
        return num_in_force(t) * w[t]
    else:
        return 0
def claims(t):
    return num_deaths(t) * S
def premiums(t):
    return num_in_force(t) * P
def net_cashflow(t):
    return premiums(t) - claims(t)
def npv(cashflow, term, int_rate):
    v = 1 / (1 + int_rate)
    return sum(cashflow(t) * v**(t+1) for t in range(term))

st.markdown(f'<h2 style="text-align: justify;">Product Definition</h2>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: justify;">Suppose we have an insurance product, in this case a simple term assurance which pays out S on death, on the condition that the policyholder pays a level premium of P per annum, and expires after T years. We also incur initial expenses of IE on setting up the policy, and renewal expenses of E per annum for the duration of the policy (this includes claim costs).</div>', unsafe_allow_html=True)
st.write("")
st.markdown(f'<h5 style="text-align: justify;">Input Variables</h4>', unsafe_allow_html=True)
kols1, kols2 = st.columns(2)
with kols1:
    P = st.number_input("P = Premium", min_value=0.00, value=100.00)
    T = st.number_input("T = Term/period (years)", min_value=0, value=10)
with kols2:
    S = st.number_input("S = Claim amount", min_value=0.00, value=25000.00)
    i = st.number_input("i = Effective rate of interest (%)", min_value=0.00, value=2.00)/100
st.write("---")

st.markdown(f'<h2 style="text-align: justify;">Modeling</h2>', unsafe_allow_html=True)
st.markdown(f'''<div style="text-align: justify;">
            
            Expected Net Value = E[PV(Premiums)] - E[PV(Claims)] - E[PV(Expenses)]
            
            ''', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: justify;">E[x] = expected value of x (in this case: arithmatic mean)</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: justify;">PV = Present Value</div>', unsafe_allow_html=True)
st.write("---")

st.markdown(f'<h2 style="text-align: justify;">Model Assumptions and Structure</h2>', unsafe_allow_html=True)
st.markdown(f'<h5 style="text-align: justify;">1. There are 3 transitions in the model</h4>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: justify;">In Force -> Claimed:'
            f' q(t) = probability of dying between time t-1 and time t, and a claim being made</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: justify;">In Force -> Lapsed:'
            f' w(t) = the probability that the policy being canceled between time t-1 and time t</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: justify;">In Force -> Expired: 1 if t is T and 0 otherwise</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: justify;">q and w are assumed to be defined as tables:</div>', unsafe_allow_html=True)
st.write("")
st.markdown(f"<div style='text-align: justify;'>q(t) and w(t) will depend on the policy holder's state (age/sex etc) and time period, but in this case are assumed to be defined as tables:</div>", unsafe_allow_html=True)

indekss = [i for i in range(T)]
if T == 10:
    q = [0.001, 0.002, 0.003, 0.003, 0.004, 0.004, 0.005, 0.007, 0.009, 0.011]
    w = [0.05, 0.07, 0.08, 0.10, 0.14, 0.20, 0.20, 0.20, 0.10, 0.04]
else:
    np.random.seed(22)
    q = []
    w = []
    startq = 0.001
    t = 1
    while t != T+1 :
        a = np.random.rand()
        q.append(startq)
        w.append(round(np.random.rand()/10,3))
        if a >= 0.35:
            startq += 0.001
        t+=1

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            .col_heading   {text-align: center !important}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)
df1 = pd.DataFrame(list(zip(indekss, q, w)), columns=["t","q","w"])
gd = GridOptionsBuilder.from_dataframe(df1)
gd.configure_pagination(enabled=True)
gd.configure_default_column(groupable=True)
gd.configure_column("t", editable=False)
gd.configure_column("q", editable=True)
gd.configure_column("w", editable=True)
gridOptions = gd.build()
grid_table = AgGrid(df1,
                    gridOptions=gridOptions,
                    fit_column_on_grid_load=True,
                    width='100%',
                    theme = 'streamlit',
                    update_mode=GridUpdateMode.GRID_CHANGED,
                    reload_data=False,
                    allow_unsafe_jscode=True,
                    editable=True)
df1 = grid_table['data']
st.markdown(f'<div style="text-align: justify;">Note: you can change the values, just give reasonable numbers</div>', unsafe_allow_html=True)
st.write("")

st.markdown(f'<h5 style="text-align: justify;">2. The expenses are ignored</h4>', unsafe_allow_html=True)
st.markdown(f'''<div style="text-align: justify;">

    P = {P}
    S = {S}
    T = {T}
    IE = 0
    E = 0
    i = {100*i}%

            ''', unsafe_allow_html=True)
st.markdown(f'<h5 style="text-align: justify;">3. The expected numbers of policies</h4>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: justify;">num_in_force = the number of policies in force</div>', unsafe_allow_html=True)
st.latex(r'''\left\{\begin{matrix}1, &  \begin{align*}
t  &= 0
\end{align*}\\
    0, &  t\geq T\\
    num\_in\_force(t-1) - num\_deaths(t-1) - num\_lapses(t-1), & otherwise
    \end{matrix}\right.''')
st.markdown(f'<div style="text-align: justify;">num_death = the number of deaths</div>', unsafe_allow_html=True)
st.latex(r'''\left\{\begin{matrix}num\_in\_force(t) \times q(t),& t<T\\
    0, & otherwise
    \end{matrix}\right.''')
st.markdown(f'<div style="text-align: justify;">num_lapses = the number of lapses occuring</div>', unsafe_allow_html=True)
st.latex(r'''\left\{\begin{matrix}num\_in\_force(t) \times w(t),& t<T\\
    0, & otherwise
    \end{matrix}\right.''')


nif = []
for t in range(T+1):
    nif.append(round(num_in_force(t),3))
time = [i for i in range(T+1)]
claim = []
prem = []
net_cash = []
for t in range(T+1):
    claim.append(round(claims(t),3))
    prem.append(round(premiums(t),3))
    net_cash.append(round(net_cashflow(t),3))
nd = [round(i/S,3) for i in claim]
w.append(0)
nl = [round(nif[i]*w[i],3) for i in range(T)]
nl.append(0)
st.write("---")

st.markdown(f'<h2 style="text-align: justify;">Modeling Results</h2>', unsafe_allow_html=True)
kyol1, kyol2 = st.columns(2)
df_structure = pd.DataFrame(list(zip(time, nif, nd, nl)),
                            columns=["t","num_in_force","num_deaths","num_lapses"])
kyol1.markdown(f'<h4 style="text-align: center;">Transitions Over Time</h4>', unsafe_allow_html=True)
kyol1.table(df_structure)
df_structure = pd.DataFrame(list(zip(time,claim,prem,net_cash)),
                            columns=["t","claims","premiums","net_cashflow"])
kyol2.markdown(f'<h4 style="text-align: center;">Overall Cashflow</h4>', unsafe_allow_html=True)
kyol2.table(df_structure)
margin = npv(net_cashflow, T, i) / npv(premiums, T, 0.02)
kolom1, kolom2, kolom3 = st.columns(3)
kolom1.metric("Total Premiums",round(npv(premiums, T, i),2))
kolom2.metric("Total Claims",round(npv(claims, T, i),2))
if margin > 0:
    kolom3.metric("Total Insurance Float",round(npv(net_cashflow, T, i),2), f"Margin = {round(100 * margin, 2)}% of Premium")
else:
    kolom3.metric("Total Insurance Float", round(npv(net_cashflow, T, i), 2), f"Margin = {round(100 * margin, 2)}% of Premium", delta=-1, delta_color="inverse")
st.write("---")

st.markdown(f'<h2 style="text-align: justify;">Conclusion</h2>', unsafe_allow_html=True)
if margin > 0:
    if margin < 0.1 :
        words = f"So in this case (ignoring expenses), we would expect the policy to be profitable, as the value of premiums received is expected to outweigh the value of claims paid. The margin ({round(100 * margin, 2)}%) is however fairly low, so introducing expenses are likely to make the policy unprofitable."
    else:
        words = f"So in this case (ignoring expenses), we would expect the policy to be profitable, as the value of premiums received is expected to outweigh the value of claims paid with the margin {round(100 * margin, 2)}%"
else:
    words = f"The policy is not profitable (margin = {round(100 * margin, 2)}%)"
st.markdown(f'<div style="text-align: justify;">{words}</div>', unsafe_allow_html=True)

