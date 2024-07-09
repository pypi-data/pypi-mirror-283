from setuptools import setup, find_packages

setup(
    name='MotifDiff-pkg',
    version='0.5.8.6',
    packages=find_packages(),
    install_requires=[
    	'regex',
        'torch',
        'pandas',
        'numpy',
        'typer',
        'pysam',
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'getDiff = MotifDiff.MotifDiff:app',
        ],
    },
)

