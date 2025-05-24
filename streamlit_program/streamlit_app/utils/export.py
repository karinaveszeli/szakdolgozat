import io
import pandas as pd
import csv


def lada_export_csv(ladak):
    adatok = []
    for i, lada in enumerate(ladak):
        lada_tartalom = "  ".join([f"[{', '.join(map(str, item))}]" for item in lada["elemek"]])
        adatok.append([f"{i + 1}. lada", lada_tartalom])

    df = pd.DataFrame(adatok, columns=["Lada", "Tartalom"])

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, header=True, sep=";", quoting=csv.QUOTE_NONE, encoding="utf-8-sig")

    return csv_buffer.getvalue()
