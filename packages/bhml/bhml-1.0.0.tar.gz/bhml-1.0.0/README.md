# SMBH
[![A rectangular badge, half black half purple containing the text made at Code Astro](https://img.shields.io/badge/Made%20at-Code/Astro-blueviolet.svg)](https://semaphorep.github.io/codeastro/)

[![Made with NumPy](https://img.shields.io/badge/Made%20with-NumPy-blue.svg)](https://numpy.org/)

[![Powered by Matplotlib](https://img.shields.io/badge/Powered%20by-Matplotlib-blue.svg)](https://matplotlib.org/)

[![Uses SciPy](https://img.shields.io/badge/Uses-SciPy-blue.svg)](https://www.scipy.org/)

## Introduction

This package is used to constrain huge Astronomical catalogs/surveys to subsets based on redshift ranges to study the evolution of objects, and also to make subsets based on their masses or any parameter we want to study. Finally, visualize these subsets with their mean points.


## Motivation

The mass_luminosity_function is a Python package for calculating the mass-luminosity function of quasars. The mass-luminosity function is an important statistical relationship between the masses of supermassive black holes (SMBHs) at the centers of galaxies and the luminosities of the quasars


## Installation

The package is installable on Python 3.x and can be installed using:

```pip install SMBH```

## Use Example and Description of Function

The mass_luminosity_function (SMBH) package includes some functions, to load the data and then calculate and plot the mass-luminosity function for quasars to know its evolution over cosmic time.
Here's an example of how to use it:

```
from bhml import entry
from bhml import classify
from bhml import submean
from bhml import visual

# from bhml import entry
# Load observational data
data = entry(RA,DEC,Z,M,LB, Me,Le)    #Add all the parameters you may need from the catalog


# from bhml import classify
#classify the quasars into subsets with specific redshift bins, in each redshift bin you could make subsets of any parmater you want in our example we made it for masses
Z_ranges = [(0.0, 1.0), (1.0, 2.0), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)]
M_ranges = [(3, 7.5), (7.5, 8.5), (8.5, 9.5), (9.5, 11.5)]
subsets = classify(data, Z_ranges, M_ranges) 

# from bhml import submean

from bhml import visual

