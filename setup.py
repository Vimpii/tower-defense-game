from setuptools import setup, find_packages

setup(
    name='tower-defense-game',
    version='1.0',
    packages=find_packages(),
    description='A tower defense game',
    author='Gyuris Martin',
    author_email='h260480@stud.u-szeged.hu',
    url='https://github.com/Vimpii/tower-defense-game',
    install_requires=[
        'pygame'
    ],
)