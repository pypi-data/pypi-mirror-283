from setuptools import setup, find_packages

setup(
    name="transformars",
    version="4.42.3-4",
    description="A drop-in replacement for the transformers library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Robert Paulson",
    author_email="bob@fclub.org",
    url="https://github.com/sudoaza/transformars",
    packages=find_packages(),
    install_requires=[
        "transformers==4.42.3",
    ],
    package_data={
        'transformars': ['bert.safertensors'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
