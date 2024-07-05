# spectral preprocessing methods
import numpy as np
from ipdb import set_trace

def snv(x):
    """ standard normal variate transformation 

    Args:
        x (np.array): spectra matrix of shape (n_samples, n_features)
    """

    x = (x - x.mean(axis=1)[:, None]) / x.std(axis=1)[:, None]

    return x

def abs2ref(x, base=10):
    """ apparent absorbance to reflectance

    Args:
        x (np.array): spectra matrix of shape (n_samples, n_features)
    """

    x = 1 / (base**x)

    return x

def ref2abs(x, base=10):
    """ reflectance to apparent absorbance

    Args:
        x (np.array): spectra matrix of shape (n_samples, n_features)

    Returns:
        np.array: absorbance spectra matrix
    """
    
    x = np.emath.logn(base, 1/x)

    return x

def derivative(x, wrt, order=1):
    """take derivatives

    Args:
        x (np.array): spectra matrix
        wrt (_type_): take the derivative with respect to (wrt)
        order (int, optional): _description_. Defaults to 1.
    """

    return x
