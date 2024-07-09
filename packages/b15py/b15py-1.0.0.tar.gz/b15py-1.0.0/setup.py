from setuptools import setup, find_packages
setup(
    name='b15py',
    version='1.0.0',
    packages=find_packages(),
    package_data={'b15py': ['b15py.so']},
)

