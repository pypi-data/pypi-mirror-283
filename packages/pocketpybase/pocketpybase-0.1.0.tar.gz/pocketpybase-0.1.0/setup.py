from setuptools import setup, find_packages

setup(
    name='pocketpybase',
    version='0.1.0',
    description='A Python package for interacting with PocketBase',
    author='Champ',
    author_email='cs@two02.io',
    packages=find_packages(),
    install_requires=[
        'httpx',
    ],
)