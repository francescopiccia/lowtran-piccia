# Lowtran in Python

---
## Changes wrt main repo

>We implemented a clear interface to lowtran with some additional parameters not available in the original repository, such as areosol scattering. We also removed matlab code and we will only use python.
---

LOWTRAN7 atmospheric absorption extinction model.
Updated to be platform independent and easily accessible from Python.

The main LOWTRAN program is accessible from Python by using direct memory transfers instead of the cumbersome and error-prone process of writing/reading text files.
`xarray.Dataset` high-performance, simple N-D array data is passed out, with appropriate metadata.

The ``LOWFIL`` program in reference/lowtran7.10.f was not connected as I had previously implemented my own filter function directly in Python.

The ``LOWSCAN`` spectral sampling (scanning) program in reference/lowtran7.13.f was not connected as I had no need for coarser spectral resolution.

| Python API Author | License |
| --- | --- |
| Micheal Hirsch  | MIT |


## Install

Lowtran requires a Fortran compiler and CMake.
We use `f2py` (part of `numpy`) to seamlessly use Fortran libraries from Python by special compilation of the Fortran library with auto-generated shim code.

1. If a Fortran compiler is not already installed, install Gfortran:

   * Linux: `apt install gfortran`
   * Mac: `brew install gcc`
   * Windows: use any one of Windows Subsystem for Linux, MSYS2, MinGW to get Gfortran or use Intel oneAPI.

Note: Cygwin is essentially obsolete due to Windows Subsystem for Linux. Cygwin is broken for Numpy and Gfortran and general.

2. Install Python Lowtran code

   ```sh
   pip install -e .
   ```
  

## Input
You can call the main model function `lowtran(context)` where context is a dict with this structure:
   ```python
   context = {
         "wlshort": 200, # minimum wavelenght in nm
         "wllong": 30000,# maximum wavelenght in nm
         "wlstep": 20,   # wavelenght step in nm
         "model": 5,     # card1 atmosphere model (0-7)
         "itype": 3,     # card1 path type (1-3)
         "iemsct": 2,    # card1 execution type (0-3)
         "im": 1,        # card1 scattering off/on (0-1)
         "ihaze": 5,     # card2 aerosol type (0-10)
         "iseasn": 0,    # card2 seasonal aerosol (0-2)
         "ivulc": 0,     # card2 aerosol profile and stratospheric aerosol (0-8)
         "icstl": 1,     # card2 air mass character (1-10) >> HAZE 3 ONLY
         "icld": 0,      # card2 cloud and rain models (0-20)
         "ird1": 0,      # activate optional card2C off/on (0-1) for custom path
         "zmdl": 0,      # card2C altitude layer boudnary [km]
         "p": 0,         # card2C pressure layer boundary
         "t": 0,         # card2C temperature layer boundary
         "wmol": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],      
         # card2C individual molecular species, see T11A p32
         "h1": 0,        # card3 initial altitude [km]
         "h2": 0,        # card3 final altitude [km] >> ITYPE 2 ONLY
         "angle": 0,     # card3 initial zenith angle from h1 [deg]
         "range_km": 0,  # card3 path length [km]
         "time": parse("2022-11-28T12") # specify time frame - TO BE TESTED
   }
   ```
Alternatively, you can loop over an angle vector with `loopangle(context)`:
   ```python
   "angle": [0,45,90],
   ```
If you don't want to use `card2C` parameters you can omit `ird1`, `zmdl`, `p`, `t`, and `wmol`.

If you don't want to specify `iseasn`, `ivulc`, `icstl`, `icld`, `h2`, `range_km`, `time`, they take default values (usually off).


Additional info on input parameters:
   - model (atmosphere model)
      - 0: Horizontal path with user specified parameters (itype must be 1)
      - 1: Tropical Atmosphere
      - 2: Midlatitude Summer
      - 3: Midlatitude Winter
      - 4: Subarctic Summer
      - 5: Subarctic Winter
      - 6: 1976 US Standard
      - 7: New model to be input
   - itype (path type)
      - 1: Horizontal path with constant pressure
      - 2: Vertical or slant path between two altitudes
      - 3: Vertical or slant path from ground to space
   - iemsct (execution type)
      - 0: Transmittance mode
      - 1: Thermal radiance mode
      - 2: Radiance mode with solar/lunar single scattering
      - 3: Calculates directly transmitted solar irradiance
   - im (scattering)
      - 0: Considers single scattering only
      - 1: Considers multiple scattering (iemsct must be 1 or 2)
   - ihaze (aerosol from 0 to 2 km / surface)
      - 0: No aerosol
      - 1: Rural - visibility 23 km
      - 2: Rural - visibility 5 km
      - 3: Maritime - visibility to be set with icstl
      - 4: Maritime - visibility 23 km
      - 5: Urban - visibility 5 km
      - 6: Tropospheric - visibility 50 km
      - 7: User defined - triggers additional cards - NOT IMPLEMENTED
      - 8: Fog - visibility 0.2 km
      - 9: Fog - visibility 0.5 km
      - 10: Desert - visibility from wind speed
   - iseasn (seasonal aerosol profile from 2 to 30 km)
      - 0: Same as model
      - 1: Spring-Summer
      - 2: Fall-Winter
   - ivulc (aerosol profile and extinction above 100 km - 30 to 100 km is always meteoric dust)
      - 0,1: Background stratospheric
      - 2: Moderate volcanic profile and Aged volcanic extinction
      - 3: High volcanic profile and Fresh volcanic extinction
      - 4: High volcanic profile and Aged volcanic extinction
      - 5: Moderate volcanic profile and Fresh volcanic extinction
      - 6: Moderate volcanic profile and Background strato extinction
      - 7: High volcanic profile and Background strato extinction
      - 8: Extreme volcanic profile and Fresh volcanic extinction
   - icstl (air mass cahracter, only for ihaze=3)
      - 1: Open ocean
      - 10: Stron continental influence
   - zmld (altitude of layer boundary in km - need model=0,7 or ird1=1)
   - p (pressure of layer boundary - need model=0,7 or ird1=1)
   - t (temperature of layer boundary - need model=0,7 or ird1=1)
   - wmol (individual molecular species as 12d-vector, see table 14 p31 lowtran manual - need model=0,7 or ird1=1)

## Notes

LOWTRAN7
[User manual](https://apps.dtic.mil/sti/pdfs/ADA206773.pdf)
Refer to this to understand what parameters are set to default.

### Reference

* Original 1994 Lowtran7 [Code](http://www1.ncdc.noaa.gov/pub/data/software/lowtran/)
* Original API repository [lowtran](https://github.com/space-physics/lowtran/)