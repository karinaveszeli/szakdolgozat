import numpy as np

def uj_lada_letrehozasa(dimenzioszam, max_kapacitas):

    kapacitasok = [max_kapacitas] * dimenzioszam
    return {"elemek": [], "maradek_kapacitas": kapacitasok}

def belefer_a_ladaba(elem, maradek_kapacitas):

    return all(np.array(elem) <= maradek_kapacitas)

def elem_hozzaadasa_ladahoz(elem, lada):

    lada["elemek"].append(elem)
    lada["maradek_kapacitas"] -= np.array(elem)
