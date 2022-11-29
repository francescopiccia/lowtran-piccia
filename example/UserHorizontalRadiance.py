#!/usr/bin/env python
"""
Horizontal cases are for special use by advanced users.
"""
from matplotlib.pyplot import show
from argparse import ArgumentParser
import lowtran
from lowtran.plot import irradiance
from dateutil.parser import parse


def main():
    p = ArgumentParser(description="Lowtran 7 interface")
    
    p.add_argument("-z", "--obsalt", help="altitude of observer [km]", type=float, default=0.05)
    p.add_argument("-s", "--short", help="shortest wavelength nm ", type=float, default=200)
    p.add_argument("-l", "--long", help="longest wavelength nm ", type=float, default=30000)
    p.add_argument("-step", help="wavelength step size cm^-1", type=float, default=20)
    P = p.parse_args()

    context = {
        "model": 0, # meteorogical data
        "itype": 1, # horizontal path
        "iemsct": 1, # radiance model
        "im": 1, # multiple scattering
        "ihaze": 5, # urban aerosol
        "ird1": 1, # card2C on
        "range_km": P.obsalt,
        "angle": 0,
        "zmdl": P.obsalt,
        "h1": P.obsalt,
        "wlshort": P.short,
        "wllong": P.long,
        "wlstep": P.step,
    }

    atmos = {
        "p": 949.0,
        "t": 283.8,
        "wmol": [93.96, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "time": parse("2022-11-28T12")
    }

    context.update(atmos)
    
    TR = lowtran.lowtran(context)

    irradiance(TR, context)

    show()


if __name__ == "__main__":
    main()
