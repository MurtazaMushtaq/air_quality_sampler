from setuptools import setup, find_packages

setup(
    name="air_quality_sampler",
    version="1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="M Mushtaq",
    author_email="mmushtaq@sfu.ca",
    description="A Python module to sample and calculate average PM2.5 levels.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MurtazaMushtaq/air_quality_sampler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
