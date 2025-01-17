#!/usr/bin/env python
"""
Total Radiance = atmosphere rad. or boundary rad. + atm. scat. or boundary refl.

Lowtran outputs W cm^-2 ster^-1 micron^-1
we want photons cm^-2 s^-1 ster^-1 micron^-1
1 W cm^-2 = 10000 W m^-2

h = 6.62607004e-34 m^2 kg s^-1
I: irradiance
Np: numer of photons
Np = (Ilowtran*10000)*lambda_m/(h*c)
"""
from pathlib import Path
from matplotlib.pyplot import show
from argparse import ArgumentParser
import lowtran
from lowtran.plot import radiance


def main():
    p = ArgumentParser(description="Lowtran 7 interface")
    p.add_argument("-z", "--obsalt", help="altitude of observer [km]", type=float, default=0.0)
    p.add_argument(
        "-a",
        "--zenang",
        help="Observer zenith angle [deg] ",
        nargs="+",
        type=float,
        default=[0.0, 60, 80],
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
        "h1": P.obsalt,  # of observer
        "itype": 3, # path to space
        "iemsct": 1, # thermal radiance
        "im": 0, # single scattering
        "ihaze": 5, # urban aerosol
        "angle": P.zenang,  # of observer
        "wlshort": P.short,
        "wllong": P.long,
        "wlstep": P.step,
    }

    TR = lowtran.loopangle(context)

    radiance(TR, context, True)

    show()


if __name__ == "__main__":
    main()
