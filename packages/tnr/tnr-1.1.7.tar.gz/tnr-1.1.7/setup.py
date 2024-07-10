from setuptools import setup, find_packages

setup(
    name="tnr",
    version="1.1.7",
    package_dir={"": "src"},  # Specify the root directory for packages
    packages=find_packages(where="src"),  # Tell setuptools to find packages under src
    include_package_data=True,  # Include other files specified in MANIFEST.in
    install_requires=[
        "Click>=8.0",  # Specify a minimum version if needed
        "requests>=2.2",  # Same here, adjust the version as per your compatibility requirements
        "cryptography>=40.0",  # Adjust based on the features you're using
        "colorama>=0.4.0",  # Add a version constraint to ensure compatibility
        "distro>=1.7.0",  # Specify according to the functionalities you need
    ],
    entry_points={"console_scripts": ["tnr=thunder.thunder:cli"]},
)

# delete old dist folder first, and increment version number

# to build: python setup.py sdist bdist_wheel
# to distribute: twine upload dist/*
