import numpy as np

#Csak dinamikus lada alapu sulyok
def suly_lada_atlag(ladak, dimenzioszam):
    if not ladak:
        return np.ones(dimenzioszam)

    maradekok = np.array([lada["maradek_kapacitas"] for lada in ladak])
    return np.mean(maradekok, axis=0)

def suly_lada_expo(ladak, dimenzioszam):
    if not ladak:
        return np.ones(dimenzioszam)

    atlag = suly_lada_atlag(ladak, dimenzioszam)
    korlatozott = np.clip(0.01 * atlag, a_min=None, a_max=10)
    return np.exp(korlatozott)


def suly_lada_reciprok(ladak, dimenzioszam):
    if not ladak:
        return np.ones(dimenzioszam)

    atlag = suly_lada_atlag(ladak, dimenzioszam)
    with np.errstate(divide='ignore', invalid='ignore'):
        reciprok = np.where(atlag > 1e-6, 1.0 / atlag, 0.0)
    reciprok = np.nan_to_num(reciprok, nan=0.0, posinf=0.0, neginf=0.0)

    reciprok = np.clip(reciprok, 0.05, 2.0)

    return reciprok



