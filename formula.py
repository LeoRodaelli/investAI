import numpy as np

def diff_2nd_order(data):
    diff_1st_order = np.diff(data)  # Diferenciação de primeira ordem
    diff_2nd_order = np.diff(diff_1st_order)  # Diferenciação de segunda ordem
    return diff_2nd_order

def sqrt_custom(data):
    return np.sqrt(data.astype(float))
