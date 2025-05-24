import streamlit as st


st.markdown("""
    <style>
    ul[data-testid="stSidebarNavItems"] li {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


# --- OLDALAK DEFINIÁLÁSA ---
main_page = st.Page(
    page="streamlit_app/pages/main_page.py",
    title="Főoldal",
    icon=":material/home:",
    default=True
)

project_1_page = st.Page(
    page="streamlit_app/pages/vbpsolver_page.py",
    title="Algoritmusfuttató alkalmazás",
    icon=":material/package_2:"
)

project_2_page = st.Page(
    page="streamlit_app/pages/benchmark_page.py",
    title=" Tesztpéldány Generátor",
    icon=":material/bar_chart:"
)
project_3_page = st.Page(
    page="streamlit_app/pages/lowerbounds_page.py",
    title="Alsó Korlát Számítás",
    icon=":material/bar_chart:"
)


# --- NAVIGÁCIÓ ELINDÍTÁSA ---
pg = st.navigation(pages=[main_page, project_1_page, project_2_page, project_3_page])
pg.run()

