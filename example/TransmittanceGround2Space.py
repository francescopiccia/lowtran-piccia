#!/usr/bin/env python
from matplotlib.pyplot import show
from argparse import ArgumentParser
import lowtran
from lowtran.plot import transmission


def main():
    p = ArgumentParser(description="Lowtran 7 interface")
    p.add_argument("-z", "--obsalt", help="altitude of observer [km]", type=float, default=0.0)
    p.add_argument(
        "-a",
        "--zenang",
        help="observer zenith angle [deg]",
        type=float,
        nargs="+",
        default=[0, 60, 80],
    )
    p.add_argument("-s", "--short", help="shortest wavelength nm ", type=float, default=200)
    p.add_argument("-l", "--long", help="longest wavelength cm^-1 ", type=float, default=30000)
    p.add_argument("-step", help="wavelength step size cm^-1", type=float, default=20)
    p.add_argument(
        "--model", 
        help='0-6, see Card1 "model" reference. 5=subarctic winter',
        type=int,
        default=5,
    )
    P = p.parse_args()

    context = {
        "wlshort": P.short, # minimum wavelenght in nm
        "wllong": P.long,# maximum wavelenght in nm
        "wlstep": P.step,   # wavelenght step in nm
        "model": P.model,     # card1 atmosphere model (0-7)
        "itype": 3,     # card1 path type (1-3)
        "iemsct": 0,    # card1 execution type (0-3)
        "im": 1,        # card1 scattering off/on (0-1)
        "ihaze": 5,     # card2 aerosol type (0-10)
        "h1": P.obsalt,        # card3 initial altitude [km]
        "angle": P.zenang,     # card3 initial zenith angle from h1 [deg]
    }
    TR = lowtran.loopangle(context)

    transmission(TR, context)

    show()


if __name__ == "__main__":
    main()
