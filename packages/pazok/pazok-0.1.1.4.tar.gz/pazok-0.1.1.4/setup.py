import re

from setuptools import setup, find_packages
with open('README.rst', encoding='utf-8') as f:
    readme = f.read()
setup(
    name='pazok',
    version='0.1.1.4',
    author='b_azo',
    author_email='husseun.selt@gmail.com',
    description='A short description of my package',
    long_description=readme,
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
