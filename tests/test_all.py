#!/usr/bin/env python
from numpy.testing import assert_array_almost_equal,run_module_suite
#
import lowtran

def test_atmosphere_transmission():

    c1={'h1':0.,'angle':0,'wlnmlim':(500,900),'model':5,'itype':3,'iemsct':0,'im':0,
        'iseasn':0,'ird1':0,'range_km':0,'zmdl':0,'p':0,'t':0,
        'wmol':[0]*12}

    TR = lowtran.golowtran(c1)

    assert_array_almost_equal([900.090027,  500.],TR.wavelength_nm[[0,-1]])
    assert_array_almost_equal([0.87720001, 0.85709256],TR.loc[:,'transmission'][[0,-1]])

def test_scatter():
    vlim = (400,700)
    angles = 60

    c1={'model':5,
        'h1': 0, # of observer
        'angle': angles, # of observer
        'wlnmlim': vlim,
        }
# %%
    TR = lowtran.scatter(c1)

    assert_array_almost_equal((700,399.988572),TR.wavelength_nm[[0,-1]])
    assert_array_almost_equal([0.876713, 0.4884],
                              TR.loc[angles,:,'transmission'][[0,-1]])
    assert_array_almost_equal([0.005259, 0.005171],
                              TR.loc[angles,:,'pathscatter'][[-10,-1]])

def test_irradiance():
    vlim = (200,25000)
    angles = 60

    c1={'model':5,
        'h1': 0, # of observer
        'angle': angles, # of observer
        'wlnmlim': vlim,
        }
# %%
    TR = lowtran.irradiance(c1)

    assert_array_almost_equal(vlim[::-1],TR.wavelength_nm[[0,-1]])
    assert_array_almost_equal([1.675140e-04, 0.9388928],
                              TR.loc[angles,:,'transmission'][[0,100]])
    assert_array_almost_equal([1.489084e-05, 3.904406e-05],
                              TR.loc[angles,:,'irradiance'][[100,1000]])


def test_radiance():
    vlim = (200,25000)
    angles = 60

    c1={'model':5,
        'h1': 0, # of observer
        'angle': angles, # of observer
        'wlnmlim': vlim,
        }
# %%
    TR = lowtran.radiance(c1)

    assert_array_almost_equal(vlim[::-1],TR.wavelength_nm[[0,-1]])
    assert_array_almost_equal([1.675140e-04, 0.9388928],
                              TR.loc[angles,:,'transmission'][[0,100]])
    assert_array_almost_equal([0.000191, 0.000261],
                              TR.loc[angles,:,'radiance'][[10,200]])

if __name__ == '__main__':
    run_module_suite()
