from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="furtheredge",
    version="0.1.3",
    description="""furtheredge-modules""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Novacture",
    author_email="amine.zemni@novacture.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=required,
    include_package_data=True,
    # url="https://github.com/Novacture/furtheredge-modules",
)
