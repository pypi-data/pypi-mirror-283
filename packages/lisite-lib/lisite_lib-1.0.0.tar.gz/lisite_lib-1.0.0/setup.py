# lisite_lib/setup.py

from setuptools import setup, find_packages

setup(
    name='lisite_lib',
    version='1.0.0',
    author='Lisite',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
