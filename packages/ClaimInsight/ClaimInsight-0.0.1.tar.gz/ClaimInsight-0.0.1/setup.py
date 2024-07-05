from setuptools import setup, find_packages

setup(
    name="ClaimInsight",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv",
        "nltk",
    ],
    author="Mohd Arshad",
    author_email="mdarshad1000@gmail.com",
    description="A library for extracting claims from various types of records",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mdarshad/ClaimInsight",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
