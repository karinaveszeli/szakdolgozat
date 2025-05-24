import numpy as np
from sulyok import suly_lada_atlag, suly_lada_expo, suly_lada_reciprok
from pontszamok import dot_product1, dot_product2, l2_norm_slack

def rendezesi_elv(elv_tipus, elemek):

    if elv_tipus == "sum":
        return sorted(elemek, key=lambda x: sum(x), reverse=True)
    elif elv_tipus == "prod":
        return sorted(elemek, key=lambda x: np.prod(np.array(x)), reverse=True)
    elif elv_tipus == "avg":
        return sorted(elemek, key=lambda x: sum(x) / len(x), reverse=True)
    else:
        raise ValueError(f"Hiba tortent a rendezes soran")

def sulyozas_kiszamitasa(sulytipus, ladak, dimenzioszam):
    if ladak is None:
        raise ValueError("Hiba")

    if sulytipus == "average":
        return suly_lada_atlag(ladak, dimenzioszam)
    elif sulytipus == "exponential":
        return suly_lada_expo(ladak, dimenzioszam)
    elif sulytipus == "reciprocal_average":
        return suly_lada_reciprok(ladak, dimenzioszam)
    else:
        raise ValueError(f"Ismeretlen suly")



def pontszamitas(pontszam_tipus, elem, lada_maradek, sulyok):

    if pontszam_tipus == "dot_product1":
        return dot_product1(elem, lada_maradek, sulyok)
    elif pontszam_tipus == "dot_product2":
        return dot_product2(elem, lada_maradek, sulyok)
    elif pontszam_tipus == "l2_norm_of_slacks":
        return l2_norm_slack(elem, lada_maradek, sulyok)
    else:
        raise ValueError(f"Ismeretlen pontszam")
