from setuptools import setup, find_packages

setup(
    name="ak_ifa",  
    version="0.1.0",
    author="Aviad Klein",
    author_email="aviad.klein@gmail.com",
    description="Incremental Feature Analysis Tool",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/AviadKlein/ifa",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)