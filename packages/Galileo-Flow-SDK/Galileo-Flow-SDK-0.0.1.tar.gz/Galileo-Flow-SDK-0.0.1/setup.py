
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Reading a flow rate from Galileo Flow Sensor'

# Setting up
setup(
    name="Galileo-Flow-SDK",
    version=VERSION,
    author="Galileo (MIC)",
    author_email="<galileo@microfluidic.fr>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['time', 'os', 'pyserial', 'struct'],
    keywords=['python', 'galileo'],
)
