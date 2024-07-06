from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vfm",
    version="0.0.1",
    author="José Torraca, Daniel Silva",
    author_email="j.neto23@imperial.ac.uk, dmsilva@peq.coppe.ufrj.br",
    description="Virtual Flow Metering - Delumping extension, suitable for the SmartMonitor platform, part of the Petrobras - Replicantes IV project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LADES-PEQ/vfm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
