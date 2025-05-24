import matplotlib.pyplot as plt
import streamlit as st

def lada_vizualizacio(ladak, max_kapacitas=1000):

    fig, ax = plt.subplots(figsize=(12, len(ladak) * 1.2))

    szinek = ['limegreen', 'gold', 'deepskyblue', 'coral', 'orchid', 'lightseagreen', 'plum', 'peru', 'pink', 'lightblue']

    for idx, lada in enumerate(ladak):
        startok = [0] * len(lada['elemek'][0])
        for elem_idx, elem in enumerate(lada['elemek']):
            szin = szinek[elem_idx % len(szinek)]

            dim_count = len(elem)

            if dim_count <= 2:
                bar_height = 0.25
                offset = 0.3
            else:
                bar_height = 0.15
                offset = 0.18

            center_shift = (dim_count - 1) * offset / 2

            for dim_idx, meret in enumerate(elem):
                ax.barh(
                    y=idx - (dim_idx * offset) + center_shift,
                    width=meret,
                    left=startok[dim_idx],
                    height=bar_height,
                    color=szin,
                    edgecolor='black'
                )
                startok[dim_idx] += meret

    # Tengelyek
    ax.invert_yaxis()
    ax.set_xlim(0, max_kapacitas)
    if max_kapacitas <= 1000:
        lepeskoz = 100
    else:
        lepeskoz = 500
    ax.set_xticks(range(0, max_kapacitas + lepeskoz, lepeskoz))
    ax.set_xlabel("Kapacitás")
    ax.set_yticks(range(len(ladak)))
    ax.set_yticklabels([f"Láda {i+1}" for i in range(len(ladak))])
    ax.set_title("Ládák vizualizációja")
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    st.pyplot(fig, clear_figure=True)
