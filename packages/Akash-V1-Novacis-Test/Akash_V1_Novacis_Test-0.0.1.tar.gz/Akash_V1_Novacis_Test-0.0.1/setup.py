from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Akash_V1_Novacis_Test",  # Replace with your own package name
    version="0.0.1",
    author="Akash V Novacis",
    author_email="akash.velpandiyan@novacisdigital.com",
    description="Test publish",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/example_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
