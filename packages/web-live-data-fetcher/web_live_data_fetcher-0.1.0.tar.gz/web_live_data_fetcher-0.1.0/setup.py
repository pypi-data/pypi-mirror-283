from setuptools import setup, find_packages

setup(
    name="web_live_data_fetcher",
    version="0.1.0",
    description="A package for retrieving and summarizing live data from web searches.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Madhan Mohan Reddy P",
    author_email="pmadhan006@gmail.com",
    url="https://github.com/MadhanMohanReddy2301/web_live_data_fetcher",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "googlesearch-python"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
