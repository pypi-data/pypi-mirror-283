from setuptools import setup, find_packages

setup(
    name="gcp_proxy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Barak Shefer",
    author_email="barakshfr@gmail.com",
    description="A package to set up a python proxy for GCP functions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gcp_proxy_package",
)