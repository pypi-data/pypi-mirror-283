from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pazok',
    version='0.1.1.7',
    author='b_azo',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)

