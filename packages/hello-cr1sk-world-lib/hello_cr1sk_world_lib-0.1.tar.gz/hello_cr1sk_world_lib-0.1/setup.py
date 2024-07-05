from setuptools import setup, find_packages

setup(
    name="hello_cr1sk_world_lib",  # Change to the new name
    version="0.1",
    packages=find_packages(),
    description="A simple library that prints 'Hello, World!'",
    author="Gabriel",
    author_email="gabr.fern99@gmail.com",
    url="https://github.com/gabrfern99/hello_cr1sk_world_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
