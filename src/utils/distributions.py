import numpy as np


def cdf(x):

    Nx = np.exp(-(x ** 2) / 2) / (2 * 3.14159265358979) ** 0.5
    vk = 1 / (1 + 0.33267 * abs(x))
    fpDistNormal = Nx * (0.4361836 * vk - 0.1201676 * vk ** 2 + 0.937298 * vk ** 3)

    if x > 0:
        fpDistNormal = 1 - fpDistNormal

    return fpDistNormal


def cdf_p(x):

    return(1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x ** 2)