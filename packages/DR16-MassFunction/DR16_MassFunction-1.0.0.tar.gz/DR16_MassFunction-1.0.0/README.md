# SMBH
[![A rectangular badge, half black half purple containing the text made at Code Astro](https://img.shields.io/badge/Made%20at-Code/Astro-blueviolet.svg)](https://semaphorep.github.io/codeastro/)

## Introduction and Motivation

The mass_luminosity_function is a Python package for calculating the mass-luminosity function of quasars. The mass-luminosity function is an important statistical relationship between the masses of supermassive black holes (SMBHs) at the centers of galaxies and the luminosities of the quasars

## Installation

The package is installable on Python 3.x and can be installed using:

```pip install SMBH```

## Use Example and Description of Function

The mass_luminosity_function (SMBH) package includes some functions, to load the data and then calculate and plot the mass luminosity function for quasars to know its evolution over cosmic time.
Here's an example of how to use it:

```
from SMBH import entery
from SMBH import classify
from SMBH import Mmean
from SMBH import Bmean

# Load observational data
data = entery(RA,DEC,Z,M,LB)

#classify the quasars to subsets at different redshifts and masses
subsets = classify(data)

# Plot the mass-luminosity function
```
