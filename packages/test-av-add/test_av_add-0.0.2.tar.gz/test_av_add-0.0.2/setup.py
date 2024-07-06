from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="test_av_add",
    version="0.0.2",
    author="Akash V",
    author_email="akash.velpandiyan@novacisdigital.com",
    description="A small test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/mypackage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
