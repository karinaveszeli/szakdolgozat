import streamlit as st
import pandas as pd
import random

def benchmark_generalas(elemek_szama, intervallumok):

    return [
        [random.randint(r[0], r[1]) for r in intervallumok]
        for _ in range(elemek_szama)
    ]

st.title("Tesztpéldány Készítő Alkalmazás")


if "szakaszok" not in st.session_state:
    st.session_state.szakaszok = []


if st.button("Új szakasz hozzáadása"):
    st.session_state.szakaszok.append({"elemek_szama": 10, "intervallumok": [(1, 100), (1, 100)]})


for i, szakasz in enumerate(st.session_state.szakaszok):
    with st.expander(f"{i + 1}. szakasz beállításai"):

        if st.button(f"Szakasz törlése", key=f"torles_{i}"):
            st.session_state.szakaszok.pop(i)
            st.rerun()
            break

        elemek_szama = st.number_input(f"{i + 1}. szakasz - Elemszám", min_value=1, value=szakasz["elemek_szama"],
                                       key=f"elemek_szama_{i}")
        dimenziok_szama = st.number_input(f"{i + 1}. Dimenziók száma", min_value=1, max_value=10,
                                          value=len(szakasz["intervallumok"]), key=f"dimenziok_szama_{i}")

        intervallumok = []
        for d in range(dimenziok_szama):
            col1, col2 = st.columns(2)
            with col1:
                min_ertek = st.number_input(f"{d + 1}. dimenzió minimum", key=f"min_{i}_{d}",
                                            value=szakasz["intervallumok"][d][0] if d < len(szakasz["intervallumok"]) else 1)
            with col2:
                max_ertek = st.number_input(f"{d + 1}. dimenzió maximum", key=f"max_{i}_{d}",
                                            value=szakasz["intervallumok"][d][1] if d < len(szakasz["intervallumok"]) else 100)
            intervallumok.append((min_ertek, max_ertek))

        szakasz["elemek_szama"] = elemek_szama
        szakasz["intervallumok"] = intervallumok


# Benchmark generálás
if st.button("Tesztpéldány generálása"):
    osszes_elem = []
    for szakasz in st.session_state.szakaszok:
        adatok = benchmark_generalas(szakasz["elemek_szama"], szakasz["intervallumok"])
        osszes_elem.extend(adatok)

    if osszes_elem:
        dimenziok_szama = len(osszes_elem[0])
        df = pd.DataFrame(osszes_elem, columns=[f"{i + 1}D" for i in range(dimenziok_szama)])

        # keverés
        keveres = st.checkbox("Véletlenszerű keverés", value=True)
        if keveres:
            df = df.sample(frac=1).reset_index(drop=True)

        st.success("Kész!")
        st.dataframe(df)

        # Letöltés
        csv = df.to_csv(index=False, sep=';').encode("utf-8")
        st.download_button(
            label="Tesztpéldány letöltése CSV formátumban",
            data=csv,
            file_name="test.csv",
            mime="text/csv"
        )
