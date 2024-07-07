from setuptools import setup, find_packages

desc = open("README.md", "r", encoding="UTF-8").read()

setup(
    name='WhatPulse-API-Py',
    version='0.2.5.2',
    packages=find_packages(),
    description='Easy Module to work with WhatPulse Client API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Flörian',
    author_email='iaccidentlyatekerosin@gmail.com',
    license='GNU General Public License v3.0 or later',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='WhatPulse',
    install_requires=[],
)