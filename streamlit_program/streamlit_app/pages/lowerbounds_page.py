import streamlit as st
import pandas as pd
from streamlit_app.utils.ellenorzes import max_kapacitas_ellenorzes
import os
from io import BytesIO



st.title("📈 Alsó Korlát Számítás")

st.markdown("""
A program az alábbi szempontok szerint határozza meg az alsó korlátot:

- Összesíti az elemek méretét dimenziónként, majd elosztja a maximális kapacitással (felfelé kerekítve).
- Megszámolja, hány olyan elem van, amelynek mérete nagyobb a maximális kapacitás **50%-ánál**.
- Megszámolja, hány olyan elem van, amelynek mérete nagyobb a maximális kapacitás **33%-ánál**, majd az így kapott darabszámot **leosztja kettővel** (és felfelé kerekíti).

A küszöbértékek dinamikusan kerülnek meghatározásra a maximális kapacitás arányában (50% és 33%).  
A végső alsó korlát a fenti értékek közül a legnagyobb.



""")

mappa_utvonal = st.text_input("Add meg a feldolgozandó mappa elérési útját (pl. C:/benchmark/2d)", value="")

if mappa_utvonal:
    fejlec_van_mappa = st.checkbox("Van fejléc a fájlokban?", value=True, key="fejlec_mappa")
    dimenzioszam_mappa = st.selectbox("Dimenziók száma", [2, 3, 4], key="dim_mappa")
    max_kapacitas_mappa = st.number_input("Maximális kapacitás", min_value=1, value=1000, key="kap_mappa")

    if st.button("Fájlok beolvasása és számítás"):
        if not os.path.exists(mappa_utvonal):
            st.error("Hiba történt a beolvasás során, a mappa nem található.")
            st.stop()

        eredmenyek = []

        for root, _, files in os.walk(mappa_utvonal):
            for file in files:
                if file.endswith(".csv"):
                    try:
                        path = os.path.join(root, file)
                        df = pd.read_csv(path, sep=";", header=0 if fejlec_van_mappa else None)
                        df = df.iloc[:, :dimenzioszam_mappa]

                        if not max_kapacitas_ellenorzes(df, max_kapacitas_mappa):
                            continue

                        nagy = 0.5 * max_kapacitas_mappa
                        kozepes = (1/3) * max_kapacitas_mappa

                        lb_nevek = []
                        lb_ertekek = []

                        if dimenzioszam_mappa == 2:
                            lb1 = -(-df.iloc[:, 0].sum() // max_kapacitas_mappa)
                            lb2 = -(-df.iloc[:, 1].sum() // max_kapacitas_mappa)
                            lb3 = (df.iloc[:, 0] > nagy).sum()
                            lb4 = (df.iloc[:, 1] > nagy).sum()
                            lb5 = -(-((df.iloc[:, 0] > kozepes).sum()) // 2)
                            lb6 = -(-((df.iloc[:, 1] > kozepes).sum()) // 2)

                            lb_nevek = ["LB1", "LB2", "LB3", "LB4", "LB5", "LB6"]
                            lb_ertekek = [lb1, lb2, lb3, lb4, lb5, lb6]

                        elif dimenzioszam_mappa == 3:
                            lb1 = -(-df.iloc[:, 0].sum() // max_kapacitas_mappa)
                            lb2 = -(-df.iloc[:, 1].sum() // max_kapacitas_mappa)
                            lb3 = -(-df.iloc[:, 2].sum() // max_kapacitas_mappa)
                            lb4 = (df.iloc[:, 0] > nagy).sum()
                            lb5 = (df.iloc[:, 1] > nagy).sum()
                            lb6 = (df.iloc[:, 2] > nagy).sum()
                            lb7 = -(-((df.iloc[:, 0] > kozepes).sum()) // 2)
                            lb8 = -(-((df.iloc[:, 1] > kozepes).sum()) // 2)
                            lb9 = -(-((df.iloc[:, 2] > kozepes).sum()) // 2)

                            lb_nevek = ["LB1", "LB2", "LB3", "LB4", "LB5", "LB6", "LB7", "LB8", "LB9"]
                            lb_ertekek = [lb1, lb2, lb3, lb4, lb5, lb6, lb7, lb8, lb9]

                        elif dimenzioszam_mappa == 4:
                            lb1 = -(-df.iloc[:, 0].sum() // max_kapacitas_mappa)
                            lb2 = -(-df.iloc[:, 1].sum() // max_kapacitas_mappa)
                            lb3 = -(-df.iloc[:, 2].sum() // max_kapacitas_mappa)
                            lb4 = -(-df.iloc[:, 3].sum() // max_kapacitas_mappa)
                            lb5 = (df.iloc[:, 0] > nagy).sum()
                            lb6 = (df.iloc[:, 1] > nagy).sum()
                            lb7 = (df.iloc[:, 2] > nagy).sum()
                            lb8 = (df.iloc[:, 3] > nagy).sum()
                            lb9 = -(-((df.iloc[:, 0] > kozepes).sum()) // 2)
                            lb10 = -(-((df.iloc[:, 1] > kozepes).sum()) // 2)
                            lb11 = -(-((df.iloc[:, 2] > kozepes).sum()) // 2)
                            lb12 = -(-((df.iloc[:, 3] > kozepes).sum()) // 2)

                            lb_nevek = [
                                "LB1", "LB2", "LB3", "LB4",
                                "LB5", "LB6", "LB7", "LB8",
                                "LB9", "LB10", "LB11", "LB12"
                            ]
                            lb_ertekek = [
                                lb1, lb2, lb3, lb4,
                                lb5, lb6, lb7, lb8,
                                lb9, lb10, lb11, lb12
                            ]

                        lb_final = max(lb_ertekek)
                        lb_max_nev = lb_nevek[lb_ertekek.index(lb_final)]

                        eredmenyek.append([file] + lb_ertekek + [lb_final, lb_max_nev])

                    except Exception as e:
                        st.warning(f" Hiba a(z) {file} fájlnál: {e}")

        if eredmenyek:
            oszlopok = ["Fajl neve"] + lb_nevek + ["Max", "Max tipusa"]
            df_vegso = pd.DataFrame(eredmenyek, columns=oszlopok)

            st.success("Feldolgozás kész.")
            st.dataframe(df_vegso)

            csv_buffer = BytesIO()
            df_vegso.to_csv(csv_buffer, index=False, sep=";", encoding="utf-8")
            csv_buffer.seek(0)

            st.download_button(
                label="Eredmények letöltése Excel fájlként",
                data= csv_buffer,
                file_name=f"also_korlatok_{dimenzioszam_mappa}D.csv",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Hiba történt.")