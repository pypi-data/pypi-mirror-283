# setup.py

from setuptools import setup, find_packages

setup(
    name='nopacks',
    version='0.1.0',
    description='A simple test for a machine learning framework',
    author='Rtisty',
    author_email='ops.em@outlook.com',
    packages=find_packages(),
    install_requires=[
        'numpy >= 1.22',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
