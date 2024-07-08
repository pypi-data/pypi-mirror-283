from setuptools import setup, find_packages
import os

# Get the long description from the README file
current_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_directory, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='infineon_paco2_dps_lib',
    version='0.1.6',  # Update the version number
    description='Library for interfacing with Infineon PA_CO2 and DPS sensors',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Ensure this is set to 'text/markdown'
    author='Powen Ko',
    author_email='powenkoads@gmail.com',
    url='https://github.com/powenko/infineon_paco2_dps_lib',
    packages=find_packages(),
    install_requires=[
        'smbus2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
