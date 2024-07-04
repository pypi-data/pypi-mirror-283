import numpy as np

def calcular_volumen_agua(D):
    L, A, P = np.mean(D, axis=1)
    return L * A * P

