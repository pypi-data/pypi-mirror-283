from setuptools import setup, find_packages, Extension


setup(
    name='bhml',
    version="1.0.0",
    packages=find_packages(),
    install_requires=["numpy>=1.24.4", "scipy>=1.11.1", "astropy>=5.3.3", "matplotlib>=3.6.1"]
,  # Add your dependencies here
    description="constrain the evolution of a complete catalog based of redshift ranges and other paramters ranges (e.g. mass, luminosity .....)",
    uathor='Fatma Shaban',
    author_email='fatmashaban0@gmail.com',
    url='https://github.com/fatma2585/bhml',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license="LICENSE",
    incluce_package_data=True,

)
