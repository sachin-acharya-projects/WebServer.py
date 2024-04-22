from setuptools import setup
from pathlib import Path

BASE = Path(__file__).parent
long_desc = BASE / "README.md"

setup(
    name="WebServer",
    version="1.0.0",
    description="It is a python Web Framework that allow you to create web pages using HTML-like tags within python script",
    long_description=long_desc.read_text(),
    long_description_content_type="text/markdown",
    keywords="Webserver WebFramework PythonFramework",
    url="https://github.com/sachin-acharya-projects/WebServer.py",
    author="Sachin Acharya",
    author_email="webserver.py.connect@gmail.com",
    license="ISC",
    packages=["WebServer", "example"],
    install_requires=["colorama"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    package_data={"": ["example"]},
)
