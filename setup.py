from setuptools import setup, find_packages

setup(
    name="SFM-Graph-Service",
    version="1.0.0",
    description="A Social Fabric Matrix framework for modeling and forecasting changes to US commodity grain prices.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "networkx",
        # Add other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
