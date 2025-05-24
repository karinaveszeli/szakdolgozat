import numpy as np
import time
from algoritmusok.seged.lada_muveletek import uj_lada_letrehozasa, belefer_a_ladaba, elem_hozzaadasa_ladahoz
from algoritmusok.seged.seged_fuggvenyek import sulyozas_kiszamitasa, pontszamitas


def geometriai_pakolas(elemek, dimenzioszam, max_kapacitas, sulyozas_tipus="average", pontszamitas_tipus="dot_product1"):
    ladak = []

    #start = time.time()

    while elemek:
        aktualis_lada = uj_lada_letrehozasa(dimenzioszam, max_kapacitas)

        while True:
            befero_elemek = [t for t in elemek if belefer_a_ladaba(t, aktualis_lada["maradek_kapacitas"])]

            if not befero_elemek:
                break

            #Ha egy beférő elem van
            if len(befero_elemek) == 1:
                kivalasztott = befero_elemek[0]

            else:
                sulyok = sulyozas_kiszamitasa(sulyozas_tipus, ladak, dimenzioszam)


                # Ha a láda még üres
                if not aktualis_lada["elemek"]:
                    aktualis_kapacitas = max_kapacitas

                else:
                    aktualis_kapacitas = aktualis_lada["maradek_kapacitas"]

                pontszamok = [
                    pontszamitas(pontszamitas_tipus, t, aktualis_kapacitas, sulyok)
                    for t in befero_elemek
                ]


                kivalasztott = befero_elemek[np.argmax(pontszamok)]

            elem_hozzaadasa_ladahoz(kivalasztott, aktualis_lada)
            elemek.remove(kivalasztott)

        ladak.append(aktualis_lada)

        #ido = round(time.time() - start, 4)
        #print(f"geometriai_pakolas ({pontszamitas_tipus}, {sulyozas_tipus}) idő: {ido} mp")

    return ladak
