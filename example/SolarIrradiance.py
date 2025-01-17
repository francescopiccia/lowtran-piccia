#!/usr/bin/env python
"""
For Irradiance, the zenith angle is locked to the zenith angle of the sun.
Implicitly, your sensor is looking at the sun and that's the only choice per
Lowtran manual p. 36 s3.2.3.1
"""
from matplotlib.pyplot import show
from argparse import ArgumentParser
import lowtran
from lowtran.plot import irradiance


def main():
    p = ArgumentParser(description="Lowtran 7 interface")
    p.add_argument("-z", "--obsalt", help="altitude of observer [km]", type=float, default=0.0)
    p.add_argument(
        "-a",
        "--zenang",
        help="zenith angle [deg]  of sun or moon",
        nargs="+",
        type=float,
        default=[0, 60, 80],
    )
    p.add_argument("-s", "--short", help="shortest wavelength [nm]", type=float, default=200)
    p.add_argument("-l", "--long", help="longest wavelength [nm]", type=float, default=30000)
    p.add_argument("-step", help="wavelength step size [cm^-1]", type=float, default=20)
    p.add_argument(
        "--model",
        help='0-6, default 5=subarctic winter',
        type=int,
        default=5,
    )
    P = p.parse_args()

    context = {
        "model": P.model,
        "h1": P.obsalt,
        "itype": 3, # path to space
        "iemsct": 3, # solar irradiance
        "im": 0, # single scattering
        "ihaze": 5, # urban aerosol
        "angle": P.zenang,  # zenith angle of sun or moon
        "wlshort": P.short,
        "wllong": P.long,
        "wlstep": P.step,
    }

    irr = lowtran.loopangle(context)

    irradiance(irr, context, True)

    show()


if __name__ == "__main__":
    main()
