from pathlib import Path
from setuptools import find_packages, setup

setup(
    name = "fenicio",
    version = "0.0.2",
    author = "Alejo Prieto Dávalos",
    author_email = "alejoprietodavalos@gmail.com",
    packages = find_packages(),
    description = "Python SDK para la API de Fenicio https://fenicio.io/.",
    long_description = Path("README.md").read_text(),
    long_description_content_type = "text/markdown",
    url = "https://pypi.org/project/fenicio/",
    project_urls = {
        "Source": "https://github.com/AlejoPrietoDavalos/fenicio/"
    },
    python_requires = ">=3.12",
    install_requires = [
        "requests>=2.32.3",
        "pydantic>=2.8.2",
    ],
    include_package_data = True
)
