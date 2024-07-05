from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="better-gradient",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for applying various color gradients to text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/better-gradient",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
