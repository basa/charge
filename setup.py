from setuptools import setup, find_packages

setup(
    name='charge',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
    ],
)
