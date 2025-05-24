from seged.seged_fuggvenyek import rendezesi_elv
from seged.lada_muveletek import uj_lada_letrehozasa, belefer_a_ladaba, elem_hozzaadasa_ladahoz

def ffd_pakolas(elemek, dimenzioszam, max_kapacitas, strategia="lada-centrikus", rendezesi_mod="osszeg"):

    #First Fit Decreasing  algoritmus

    ladak = []
    rendezett_elemek = rendezesi_elv(rendezesi_mod, elemek)

    if strategia == "lada-centrikus":
        while rendezett_elemek:
            uj_lada = uj_lada_letrehozasa(dimenzioszam, max_kapacitas)
            eltavolitando_elemek = []

            for elem in rendezett_elemek:
                if belefer_a_ladaba(elem, uj_lada["maradek_kapacitas"]):
                    elem_hozzaadasa_ladahoz(elem, uj_lada)
                    eltavolitando_elemek.append(elem)

            rendezett_elemek = [e for e in rendezett_elemek if e not in eltavolitando_elemek]
            ladak.append(uj_lada)

    else:
        for elem in rendezett_elemek:
            elhelyezve = False

            for lada in ladak:
                if belefer_a_ladaba(elem, lada["maradek_kapacitas"]):
                    elem_hozzaadasa_ladahoz(elem, lada)
                    elhelyezve = True
                    break

            if not elhelyezve:
                uj_lada = uj_lada_letrehozasa(dimenzioszam, max_kapacitas)
                elem_hozzaadasa_ladahoz(elem, uj_lada)
                ladak.append(uj_lada)

    return ladak
