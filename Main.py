import streamlit as st
from pathlib import Path
from PIL import Image
from streamlit_extras.let_it_rain import rain


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
# resume_file = current_dir / "resume.pdf"
profile_pic = current_dir / "assets" / "pfp.png"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "Pam's Archives"
PAGE_ICON = "random"
NAME = "Pamella Cathryn"
DESCRIPTION = '''
Aspiring Actuarial Analyst, automating calculations with Python and Excel
'''
EMAIL = "pamellacathrynnnn@gmail.com"
SOCIAL_MEDIA = {
    "📩 Email" : "https://pamellacathrynnnn@gmail.com",
    "👩🏼‍💼 LinkedIn": "https://www.linkedin.com/in/pamellacathryn/",
    "👩🏼‍💻 GitHub" : "https://github.com/pamellacathryn"
}

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
rain(
    emoji="❄️",
    font_size=10,
    falling_speed=10,
    animation_length="infinite",
)
# --- LOAD CSS, PDF & PROFILE PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)
profile_pic = Image.open(profile_pic)

# --- START ---
col1, col2 = st.columns([1,2], gap="large")
with col1:
    st.image(profile_pic, width=230)
with col2:
    st.markdown("<h1 style='text-align: justify;'>Hi There!👋🏼</h1>", unsafe_allow_html=True)
    words = "I am Pam, an aspiring actuarial analyst currently studying Actuarial Science at Bandung Institute of Technology. In this Web App, I have collected all my personal projects from my college and internship experiences, and I hope you find them useful. Please do not hesitate to contact me with any feedback or requests using the links below. Thank you!💖"
    st.markdown(f'<div style="text-align: justify;">{words}</div>', unsafe_allow_html=True)
    # st.write(DESCRIPTION)
    # st.write("📍 Bandung, Indonesia")

st.write("")
st.write("")

st.subheader("Contacts 📞")
platforms = []
links = []
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    platforms.append(platform)
    links.append(link)
kol1, kol2 = st.columns([1,6])
with kol1:
    for platform in platforms:
        st.write(platform)
with kol2:
    for link in links:
        st.write(f": {link}")
