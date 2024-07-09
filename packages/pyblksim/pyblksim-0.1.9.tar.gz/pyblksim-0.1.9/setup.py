from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name='pyblksim',
    version='0.1.9',
    packages=find_packages(),
    description='An Open-Source Model Based Simulator for Discrete-Time Simulations',
    author='Dr. Kurian Polachan',
    author_email='kurian.polachan@iiitb.ac.in',
    license='GPLv3',
    install_requires=[
        'numpy',
        'matplotlib',
        'simpy',
        'scipy',
    ],
    python_requires='>=3.6',
    url='https://sites.google.com/view/cdwl/professor',
    long_description=long_description,
    long_description_content_type='text/x-rst',
)
