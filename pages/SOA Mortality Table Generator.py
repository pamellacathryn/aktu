import streamlit as st
from pymort import MortXML
import pandas as pd

st.set_page_config(
    page_title="Mortality Table",
    page_icon="💀",
    layout="centered",
    initial_sidebar_state="collapsed",
)
with st.sidebar:
    st.header("About")
    st.info("This web app is made by Pamella Cathryn. You can follow me on [LinkedIn](https://linkedin.com/in/pamellacathryn) | [Instagram](https://instagram.com/pamellacathryn) | [GitHub](https://github.com/pamellacathryn)")

list_code = pd.read_csv("assets/List_Code.csv")["Kode"].tolist()

st.markdown(f"<h1 style='text-align: center; '>SOA Mortality Table</h1>",
                unsafe_allow_html=True)
st.markdown("---")
code = st.selectbox("Input Table ID", ["Table ID 👇🏼"]+list_code)
try:
    xml = MortXML(code)
    xml_full = xml.Tables[1].Values
    starting_age = st.number_input("Input Starting Age", min_value=xml_full.index[0], max_value=xml_full.index[-1], value=xml_full.index[0], step=1)
    init_pop = st.number_input("Input Initial Population", value=1, step=1)
    st.markdown(f"<h4 style='text-align: center; '>{xml.ContentClassification.TableName}'s Mortality Table</h4>",
                unsafe_allow_html=True)
    xml_full.columns = ['q_x']
    xl = starting_age-xml_full.index[0]
    xml_crop = xml_full.iloc[xl:]
    banyak_umur = len(xml_crop)
    lx = [init_pop]
    dx = []
    lx1 = []
    for i in range(banyak_umur):
        dx.append(lx[i]*xml_crop.iloc[i])
        lx1.append(lx[i]-dx[i])
        lx.append(lx1[i][0])
    lx = lx[:-1]
    lx = pd.DataFrame(lx)
    lx.columns = ['lx']
    dx = pd.DataFrame(dx)
    dx.columns = ['dx']
    lx1 = pd.DataFrame(lx1)
    lx1.columns = ['lx1']
    full = pd.concat([xml_crop, lx.set_index(xml_crop.index), dx.set_index(xml_crop.index), lx1.set_index(xml_crop.index)],axis=1,ignore_index=True)
    full.columns = ['qx','lx','dx','lx1']
    st.table(full)
    col1, col2, col3 = st.columns([2,2,2])
    csv = full.to_csv().encode('utf-8')
    col1.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f'Mort Table {code}.csv',
        mime='text/csv',
    )
    col2.caption("qx = Probability of Death")
    col2.caption("lx = Number of Survival (BoY)")
    col3.caption("dx = Number of Death")
    col3.caption("lx1 = Number of Survival (EoY)")
except:
    st.info('Table ID from [SOA Table](https://mort.soa.org)', icon="ℹ️")

