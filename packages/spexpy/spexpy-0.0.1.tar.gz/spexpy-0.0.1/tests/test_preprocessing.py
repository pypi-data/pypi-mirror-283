import numpy as np
import pandas as pd
from pathlib import Path
import pytest
from spexpy.preprocessing import snv, abs2ref, ref2abs

# raw spectra
@pytest.fixture
def spectra():

    pdir = Path().cwd()
    ddir = pdir / 'data'

    df = pd.read_csv(ddir/'lucas_uk.csv')

    spec_arr = df.loc[:, '400':'2499.5'].to_numpy()
    return spec_arr

@pytest.mark.skip('passed')
def test_snv(spectra):

    # prepare data: spectra
    

    # run preprocessing
    spectra_snv = snv(spectra)
    # assert
    assert np.mean(spectra_snv[0, :]) < 0.001
    assert np.std(spectra_snv[0, :]) < 1.1
    assert np.std(spectra_snv[0, :]) > 0.9

@pytest.mark.skip('passed')
def test_abs2ref(spectra):

    spectra_ref = abs2ref(spectra)

    assert spectra_ref.min() > 0.0
    assert spectra_ref.max() < 1.0

def test_ref2abs(spectra):

    spectra_ref = abs2ref(spectra)
    spectra_abs = ref2abs(spectra_ref)

    assert (spectra_abs - spectra).min() < 0.001