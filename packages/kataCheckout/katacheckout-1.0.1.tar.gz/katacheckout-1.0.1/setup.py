from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Python package for kataCheckout'
LONG_DESCRIPTION = 'This is a python package for the kata 09: back to the checkout, which is a kata from codewars.com'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="kataCheckout",
    version=VERSION,
    author="Alejandro Beltre",
    author_email="alejandro.beltre134@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
