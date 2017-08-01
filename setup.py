"""A setuptools based setup module for the Biodemography Project

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Biodemography Project',

    version='1.2.0',

    # Project Description
    description='An unique method for finding conserved patterns in the different global causes of mortality',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/skchronicles/Biodemography',

    # Author details
    author='Skyler Kuhn',
    author_email='kuhnsa2@mymail.vcu.edu',

    # License
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Beta',

        # Target Audience
        'Intended Audience :: Developers, Researchers',
        'Topic :: Software Development :: Biodemography Build Tools',

        # License Information
        'License :: OSI Approved :: MIT License',

        # Supported Versions of Python
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='Biodemography Data Mining Combinatorial optimization\
     WHO Apriori Algorithm setuptools development',

    # Specifying needed packages for the project with find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List of run-time dependencies are here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['peppercorn', 'scipy', 'numpy','pandas'],

    # List of additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
       # 'dev': ['check-manifest'],
       # 'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'biodemography': ['mdlt3160_2011.csv', 'mdlt4050_2006.csv', 'mdlt4260_2010.csv',
                          'mdlt4300_2010.csv', 'mdlt4335_2005.csv', 'Sex1_mdlt3160_2011.csv',
                          'Sex1_mdlt4050_2006.csv', 'Sex1_mdlt4260_2010.csv', 'Sex1_mdlt4300_2010.csv',
                          'Sex1_mdlt4335_2005.csv', 'Sex2_mdlt3160_2011.csv', 'Sex2_mdlt4050_2006.csv',
                          'Sex2_mdlt4260_2010.csv', 'Sex2_mdlt4300_2010.csv', 'Sex2_mdlt4335_2005.csv']
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': ['biodemography=biodemography:main'],
    },
)
