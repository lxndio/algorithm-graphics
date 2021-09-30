from setuptools import find_packages, setup

setup(
    name='algorithmgraphics',
    packages=find_packages(include=['algorithmgraphics']),
    version='0.1.3',
    description='A Python library to generate graphics for explaining the functional principle of (pattern matching) algorithms.',
    author='Alexander Korn',
    license='GNU GPL-3.0',
    install_requires=['pycairo'],
)
