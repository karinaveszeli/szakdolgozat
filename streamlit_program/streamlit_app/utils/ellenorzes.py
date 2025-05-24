import streamlit as st

def max_kapacitas_ellenorzes(df, max_kapacitas):

    #Ellenőrzi, hogy az adatfájlban lévő bármely elem ne legyen nagyobb a megadott maximális kapacitásnál.

    if (df > max_kapacitas).any().any():
        st.error(f"Hiba: A feltöltött adatok között van olyan érték, ami nagyobb, mint a megadott maximális kapacitás ({max_kapacitas})!")
        return False
    return True
