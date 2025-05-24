import os
import pandas as pd
import time
from algoritmusok.ffd_pakolas import ffd_pakolas
from algoritmusok.geometriai_pakolas import geometriai_pakolas

def osszehasonlitas(input_mappa, output_fajl, dimenzioszam=2, max_kapacitas=1000):
    eredmenyek = []


    ffd_rendezesi_modok = ["sum", "prod", "avg"]
    geometriai_pontszamitasok = ["dot_product1", "dot_product2", "l2_norm_of_slacks"]
    geometriai_sulyozasok = ["average", "exponential", "reciprocal_average"]

    # fájlok beolvasása
    for gyoker, _, fajlok in os.walk(input_mappa):
        for fajlnev in fajlok:
            if not fajlnev.endswith(".csv"):
                continue

            fajl_path = os.path.join(gyoker, fajlnev)
            try:
                df = pd.read_csv(fajl_path, sep=';', header=0)
            except Exception as e:
                print(f"Hiba a fájlnál: {fajl_path} → {e}")
                continue

            elemek = [tuple(map(int, row[:dimenzioszam])) for _, row in df.iterrows()]
            relativ_path = os.path.basename(fajl_path)


            # FFD elemcentrikus
            for mod in ffd_rendezesi_modok:
                start = time.time()
                ladak = ffd_pakolas(elemek[:], dimenzioszam, max_kapacitas,
                                    strategia="Elem-centrikus", rendezesi_mod=mod)
                futasi_ido = time.time() - start
                eredmenyek.append({
                    "fajl": relativ_path,
                    "algoritmus": f"FFD_{mod}",
                    "tipus": "elem",
                    "sulyozas": "nincs",
                    "ladak_szama": len(ladak),
                    "futasi_ido_sec": round(futasi_ido, 4)
                })

            # FFD ládacentrikus
            for mod in ffd_rendezesi_modok:
                start = time.time()
                ladak = ffd_pakolas(elemek[:], dimenzioszam, max_kapacitas,
                                    strategia="Láda-centrikus", rendezesi_mod=mod)
                futasi_ido = time.time() - start
                eredmenyek.append({
                    "fajl": relativ_path,
                    "algoritmus": f"FFD_{mod}",
                    "tipus": "lada",
                    "sulyozas": "nincs",
                    "ladak_szama": len(ladak),
                    "futasi_ido_sec": round(futasi_ido, 4)
                })

            # Geometriai (dinamikus ládaalapú)
            for pont in geometriai_pontszamitasok:
                for suly in geometriai_sulyozasok:
                    start = time.time()
                    ladak = geometriai_pakolas(elemek[:], dimenzioszam, max_kapacitas,
                                               sulyozas_tipus=suly, pontszamitas_tipus=pont)
                    futasi_ido = time.time() - start
                    eredmenyek.append({
                        "fajl": relativ_path,
                        "algoritmus": pont,
                        "tipus": "lada",
                        "sulyozas": suly,
                        "ladak_szama": len(ladak),
                        "futasi_ido_sec": round(futasi_ido, 4)
                    })

    # Eredmények mentése
    df_eredmeny = pd.DataFrame(eredmenyek)
    df_eredmeny.to_csv(output_fajl, index=False, sep=';')
    print(f"Eredemeny elkeszult: {output_fajl}")



if __name__ == "__main__":
    osszehasonlitas(
        input_mappa="C:/szakdogaProgram/szakdogavegleges/tesztek/4D",
        output_fajl="eredmenyek_4d.csv",
        dimenzioszam=4,
        max_kapacitas=1000
    )

