import streamlit as st
import pandas as pd
import datetime
from algoritmusok.ffd_pakolas import ffd_pakolas
from algoritmusok.geometriai_pakolas import geometriai_pakolas
from streamlit_app.utils.export import lada_export_csv
from streamlit_app.utils.vizualizacio import lada_vizualizacio
from streamlit_app.utils.ellenorzes import max_kapacitas_ellenorzes

st.title("Algoritmus Tesztelőfelület")

feltoltott_fajl = st.file_uploader("Tölts fel egy CSV vagy Excel fájlt", type=['csv', 'xlsx'])

if feltoltott_fajl is not None:
    fejléc_van = st.checkbox("Van fejléc a fájlban?", value=True)

dimenzioszam = st.selectbox("Add meg, hány oszlopot (dimenziót) szeretnél beolvasni a fájlból", [2, 3, 4])

max_kapacitas = st.number_input("Add meg a ládák maximális kapacitását (pl. 1000):", min_value=1, value=1000)

algoritmus_tipus = st.radio("Válaszd ki az algoritmus típusát", ["Láda-centrikus", "Elem-centrikus"], index=None)


if algoritmus_tipus == "Láda-centrikus":
    algoritmus = st.selectbox("Válassz algoritmust", ["FFD Pakolás", "Geometriai Pakolás"])
    if algoritmus == "Geometriai Pakolás":
        pontszamitas_tipus = st.selectbox("Válaszd ki a pontszámítás típusát", ["dot_product1", "dot_product2", "l2_norm_of_slacks"])
        sulyozas_tipus = st.selectbox("Válaszd ki a súlyozás típusát", ["average", "exponential", "reciprocal_average"])
    elif algoritmus == "FFD Pakolás":
        rendezesi_mod = st.selectbox("Válaszd ki a rendezési módot", ["sum", "prod", "avg"])

elif algoritmus_tipus == "Elem-centrikus":
    algoritmus = st.selectbox("Válassz algoritmust", ["FFD Pakolás"])
    if algoritmus == "FFD Pakolás":
        rendezesi_mod = st.selectbox("Válaszd ki a rendezési módot", ["sum", "prod", "avg"])


if "futtatas_tortent" not in st.session_state:
    st.session_state["futtatas_tortent"] = False
if "vizualizacio_megjelenit" not in st.session_state:
    st.session_state["vizualizacio_megjelenit"] = False
if "export_megjelenit" not in st.session_state:
    st.session_state["export_megjelenit"] = False


if st.button("Futtatás"):

    if feltoltott_fajl is not None:
        header_param = 0 if fejléc_van else None

        if feltoltott_fajl.name.endswith(".csv"):
            df = pd.read_csv(feltoltott_fajl, sep=";", header=header_param)
        elif feltoltott_fajl.name.endswith(".xlsx"):
            df = pd.read_excel(feltoltott_fajl, header=header_param)

        if dimenzioszam is None:
            st.error("Kérjük válaszd ki a dimenziók számát!")
            st.stop()


        elemek = [tuple(df.iloc[i, :dimenzioszam]) for i in range(len(df))]


        if not max_kapacitas_ellenorzes(df, max_kapacitas):
            st.stop()

        # Algoritmus futtatása
        ladak = []

        if algoritmus == "FFD Pakolás":
            ladak = ffd_pakolas(elemek, dimenzioszam=dimenzioszam, max_kapacitas=max_kapacitas,
                                strategia=algoritmus_tipus, rendezesi_mod=rendezesi_mod)
        elif algoritmus == "Geometriai Pakolás":
            ladak = geometriai_pakolas(elemek, dimenzioszam=dimenzioszam, max_kapacitas=max_kapacitas,
                                       sulyozas_tipus=sulyozas_tipus, pontszamitas_tipus=pontszamitas_tipus)

        st.session_state["ladak"] = ladak
        st.session_state["futtatas_tortent"] = True
        st.session_state["vizualizacio_megjelenit"] = False
        st.session_state["export_megjelenit"] = False

    else:
        st.warning("Először tölts fel egy fájlt!")


if st.session_state["futtatas_tortent"]:

    st.subheader("Eredmények:")
    st.write(f"**Összes aktivált láda:** {len(st.session_state['ladak'])} db")
    for i, lada in enumerate(st.session_state["ladak"]):
        st.write(f"**{i + 1}. lada:** {lada['elemek']}")


    st.subheader("Vizualizáció")
    if st.button("Vizualizáció készítése"):
        st.session_state["vizualizacio_megjelenit"] = True
    if st.session_state["vizualizacio_megjelenit"]:
        lada_vizualizacio(st.session_state["ladak"], max_kapacitas)


    st.subheader("Exportálás")

    st.info("""
    Az adatok exportálásához kattints az "Eredmények exportálása" gombra.  
    Ezután megjelenik a letöltés gomb, amivel elmentheted a fájlt a számítógépedre.
    """)

    if st.button("Eredmények exportálása CSV formátumban"):
        csv_data = lada_export_csv(st.session_state["ladak"])
        st.success("Exportálás elkészült!")

        st.download_button(
            label="📥 Letöltés",
            data=csv_data,
            file_name=f"lada_pakolas_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )



