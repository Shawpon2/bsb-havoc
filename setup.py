"""
BSB Havoc Setup Configuration
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from package
with open(os.path.join("bsb_havoc", "__init__.py"), "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="bsb-havoc",
    version=version,
    author="Black Spammer Bd",
    author_email="githubshawpon@gmail.com",
    description="The World's Most Powerful Professional Load Testing Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shawpon2/bsb-havoc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Benchmark",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "colorama>=0.4.6",
        "asyncio>=3.4.3",
    ],
    entry_points={
        "console_scripts": [
            "bsb-havoc=bsb_havoc.cli:main",
            "havoc=bsb_havoc.cli:main",
            "bsb-test=bsb_havoc.cli:main",
        ],
    },
    keywords=[
        "load-testing",
        "stress-testing",
        "performance-testing",
        "benchmark",
        "ddos-testing",
        "http-testing",
        "network-testing",
        "professional",
        "powerful",
        "havoc",
    ],
    project_urls={
        "Bug Reports": "https://github.com/Shawpon2/bsb-havoc/issues",
        "Source": "https://github.com/Shawpon2/bsb-havoc",
        "Documentation": "https://github.com/Shawpon2/bsb-havoc/wiki",
    },
)
