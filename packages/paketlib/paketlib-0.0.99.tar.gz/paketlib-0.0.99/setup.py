from setuptools import setup, find_packages

setup(
    name='paketlib',
    version='0.0.99',
    description='PaketSoftware lib',
    author='PaketSoftware',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pystyle',
        'bs4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
