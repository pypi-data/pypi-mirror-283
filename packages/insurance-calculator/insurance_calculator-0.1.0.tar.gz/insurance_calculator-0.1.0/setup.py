from setuptools import setup, find_packages

setup(
    name="insurance_calculator",
    version="0.1.0",
    description="A library to calculate car insurance assurance amounts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="baluthota",
    author_email="baluthota2012@gmail.com",
    url="https://github.com/baluthota2012/test_pypl",  # Update this with your actual URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

