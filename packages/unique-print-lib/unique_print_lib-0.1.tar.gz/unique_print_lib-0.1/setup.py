from setuptools import setup, find_packages

setup(
    name="unique_print_lib",  # Unique name for your package
    version="0.1",
    packages=find_packages(),
    description="A simple library that prints different messages.",
    author="Gabriel",
    author_email="gabr.fern99@gmail.com",
    url="https://github.com/yourusername/unique_print_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
