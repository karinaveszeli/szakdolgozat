import streamlit as st
import pandas as pd
from io import BytesIO
from streamlit_app.utils.ellenorzes import max_kapacitas_ellenorzes

st.title("📈 Alsó Korlát Számítás")

st.markdown("""
A program az alábbi szempontok szerint határozza meg az alsó korlátot:

- Összesíti az elemek méretét dimenziónként, majd elosztja a maximális kapacitással (felfelé kerekítve).
- Megszámolja, hány olyan elem van, amelynek mérete nagyobb a maximális kapacitás **50%-ánál**.
- Megszámolja, hány olyan elem van, amelynek mérete nagyobb a maximális kapacitás **33%-ánál**, majd az így kapott darabszámot **leosztja kettővel** (és felfelé kerekíti).
""")

feltoltott_fajlok = st.file_uploader(
    "Tölts fel egy vagy több CSV fájlt",
    type="csv",
    accept_multiple_files=True
)

if feltoltott_fajlok:
    fejlec_van = st.checkbox("Van fejléc a fájlokban?", value=True)
    dimenzioszam = st.selectbox("Dimenziók száma", [2, 3, 4])
    max_kapacitas = st.number_input("Maximális kapacitás", min_value=1, value=1000)

    if st.button("Alsó korlátok számítása"):
        eredmenyek = []

        for file in feltoltott_fajlok:
            try:
                df = pd.read_csv(file, sep=";", header=0 if fejlec_van else None)
                df = df.iloc[:, :dimenzioszam]

                if not max_kapacitas_ellenorzes(df, max_kapacitas):
                    continue

                nagy = 0.5 * max_kapacitas
                kozepes = (1 / 3) * max_kapacitas

                lb_nevek = []
                lb_ertekek = []

                if dimenzioszam == 2:
                    lb1 = -(-df.iloc[:, 0].sum() // max_kapacitas)
                    lb2 = -(-df.iloc[:, 1].sum() // max_kapacitas)
                    lb3 = (df.iloc[:, 0] > nagy).sum()
                    lb4 = (df.iloc[:, 1] > nagy).sum()
                    lb5 = -(-((df.iloc[:, 0] > kozepes).sum()) // 2)
                    lb6 = -(-((df.iloc[:, 1] > kozepes).sum()) // 2)

                    lb_nevek = ["LB1", "LB2", "LB3", "LB4", "LB5", "LB6"]
                    lb_ertekek = [lb1, lb2, lb3, lb4, lb5, lb6]

                elif dimenzioszam == 3:
                    lb1 = -(-df.iloc[:, 0].sum() // max_kapacitas)
                    lb2 = -(-df.iloc[:, 1].sum() // max_kapacitas)
                    lb3 = -(-df.iloc[:, 2].sum() // max_kapacitas)
                    lb4 = (df.iloc[:, 0] > nagy).sum()
                    lb5 = (df.iloc[:, 1] > nagy).sum()
                    lb6 = (df.iloc[:, 2] > nagy).sum()
                    lb7 = -(-((df.iloc[:, 0] > kozepes).sum()) // 2)
                    lb8 = -(-((df.iloc[:, 1] > kozepes).sum()) // 2)
                    lb9 = -(-((df.iloc[:, 2] > kozepes).sum()) // 2)

                    lb_nevek = ["LB1", "LB2", "LB3", "LB4", "LB5", "LB6", "LB7", "LB8", "LB9"]
                    lb_ertekek = [lb1, lb2, lb3, lb4, lb5, lb6, lb7, lb8, lb9]

                elif dimenzioszam == 4:
                    lb1 = -(-df.iloc[:, 0].sum() // max_kapacitas)
                    lb2 = -(-df.iloc[:, 1].sum() // max_kapacitas)
                    lb3 = -(-df.iloc[:, 2].sum() // max_kapacitas)
                    lb4 = -(-df.iloc[:, 3].sum() // max_kapacitas)
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

                eredmenyek.append([file.name] + lb_ertekek + [lb_final, lb_max_nev])

            except Exception as e:
                st.warning(f"Hiba")

        if eredmenyek:
            oszlopok = ["Fajl neve"] + lb_nevek + ["Max", "Max tipusa"]
            df_vegso = pd.DataFrame(eredmenyek, columns=oszlopok)

            st.success("Feldolgozás kész.")
            st.dataframe(df_vegso)

            csv_buffer = BytesIO()
            df_vegso.to_csv(csv_buffer, index=False, sep=";", encoding="utf-8-sig")
            csv_buffer.seek(0)

            st.download_button(
                label="Eredmények letöltése",
                data=csv_buffer,
                file_name=f"also_korlatok_{dimenzioszam}D.csv",
                mime="text/csv"
            )
        else:
            st.warning("Nem sikerült érvényes adatot feldolgozni.")
