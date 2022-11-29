#!/usr/bin/env python
"""
Horizontal cases are for special use by advanced users.

lowtran manual p.36 specify height H1 and RANGE

Pressure [millibar]
temperature [Kelvin]
"""
from matplotlib.pyplot import show
from argparse import ArgumentParser
import lowtran
from lowtran.plot import horiz


def main():
    p = ArgumentParser(description="Lowtran 7 interface")
    p.add_argument(
        "-z",
        "--obsalt",
        help="altitude of bother observers on horizontal path [km]",
        type=float,
        default=0.3,
    )
    p.add_argument(
        "-r",
        "--range_km",
        help="range between observers on horizontal path [km]",
        type=float,
        default=1.0,
    )
    p.add_argument(
        "-a",
        "--zenang",
        help="zenith angle [deg]  can be single value or list of values",
        type=float,
        default=0.0,
    )
    p.add_argument("-s", "--short", help="shortest wavelength [nm]", type=float, default=200)
    p.add_argument("-l", "--long", help="longest wavelength [nm]", type=float, default=30000)
    p.add_argument("-step", help="wavelength step size [cm^-1]", type=float, default=20)
    P = p.parse_args()

    context = {
        "model": 5, # default
        "itype": 1, # horizontal path
        "iemsct": 0, # tx model
        "im": 0, # user-defined horizontal model
        "ird1": 1, # card2C on
        "ihaze": 5, # urban aerosol
        "zmdl": P.obsalt,
        "h1": P.obsalt,
        "range_km": P.range_km,
        "angle": 0,
        "wlshort": P.short,
        "wllong": P.long,
        "wlstep": P.step,
    }

    atmos = {
        "p": 949.0,
        "t": 283.8,
        "wmol": [93.96, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    }

    context.update(atmos)

    TR = lowtran.lowtran(context).squeeze()

    horiz(TR, context)

    show()


if __name__ == "__main__":
    main()
