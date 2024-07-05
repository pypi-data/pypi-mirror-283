from setuptools import setup, find_packages

setup(
    name="enterpret_claims_extractor",
    version="0.1.1",
    author="Mohd Arshad",
    author_email="mdarshad1000@gmail.com",
    description="A tool for extracting claims from various types of records",
    url="https://github.com/mdarshad1000/enterpret_claims_extractor",
    packages=find_packages(),
    install_requires=[
        "openai",
        "nltk",
    ],
    python_requires=">=3.7",
)