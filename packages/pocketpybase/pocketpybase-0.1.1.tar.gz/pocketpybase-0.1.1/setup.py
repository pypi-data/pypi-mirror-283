from setuptools import setup

setup(
    name='pocketpybase',
    version='0.1.1',
    description='A Python package for interacting with PocketBase',
    author='Champ',
    author_email='cs@two02.io',
    packages=['pocketbase', 'pocketbase.deps', 'pocketbase.db'],
    install_requires=[
        'httpx',
    ],
)