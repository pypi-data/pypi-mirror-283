from setuptools import setup, find_packages

setup(
    name="base64Compressor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow"
    ],
    entry_points={
        "console_scripts": [
            "base64Compressor=base64Compressor.__main__:main",
        ],
    },
    author="Aditya Rachman",
    author_email="adityarachman24.ar@gmail.com",
    description="A library to compress base64 encoded images.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adityarach/base64Compressor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
