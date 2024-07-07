from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="secure-encryption",
    version="0.0.1",
    author="Mohammed Irfanul Alam Tanveer",
    author_email="irfanulalamtanvir@gmail.com",
    description="A simple and secure encryption service for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/irfanul/secure-encryption-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pycryptodome',
    ],
)
