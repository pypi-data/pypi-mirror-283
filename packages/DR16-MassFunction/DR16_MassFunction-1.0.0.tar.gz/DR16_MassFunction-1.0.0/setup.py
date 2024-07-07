from setuptools import setup, find_packages, Extension
import numpy

setup(
    name='DR16_MassFunction',
    version="1.0.0",
    description="calculating the mass-luminosity functions of quasars on any complete catalog",
    packages=find_packages(),
    license="LICENSE",
    incluce_package_data=True,

)
