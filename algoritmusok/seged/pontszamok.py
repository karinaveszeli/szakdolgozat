import numpy as np

def dot_product1(elem, lada_maradek, sulyok):

    #Dot Product 1

    szorzatok = np.array(sulyok) * np.array(elem) * np.array(lada_maradek)
    if np.any(np.isnan(szorzatok)) or np.any(np.isinf(szorzatok)):
        return -np.inf
    return np.sum(szorzatok)

def dot_product2(elem, lada_maradek, sulyok):

    #Dot Product 2

    dot_prod = dot_product1(elem, lada_maradek, sulyok)
    norma_elem = np.linalg.norm(elem)
    norma_lada = np.linalg.norm(lada_maradek)

    if norma_elem <= 1e-8 or norma_lada <= 1e-8:
        return 0

    eredmeny = dot_prod / (norma_elem * norma_lada)
    if np.isnan(eredmeny) or np.isinf(eredmeny):
        return -np.inf
    return eredmeny

def l2_norm_slack(elem, lada_maradek, sulyok):

    #L2-Norm of Slacks

    slack = np.array(lada_maradek) - np.array(elem)
    sulyozott_slack = np.array(sulyok) * (slack ** 2)

    if np.any(np.isnan(sulyozott_slack)) or np.any(np.isinf(sulyozott_slack)):
        return -np.inf

    return -np.sum(sulyozott_slack)
