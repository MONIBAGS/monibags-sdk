"""
MoniBags SDK - Twitter Username History Checker
Setup configuration for pip installation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="monibags",
    version="1.0.0",
    author="MoniBags",
    author_email="noreply@monibags.xyz",
    description="SDK for MoniBags Twitter Username History Checker API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monibags/monibags-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "monibags=monibags.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/monibags/monibags-sdk/issues",
        "Source": "https://github.com/monibags/monibags-sdk",
        "Documentation": "https://monibags.xyz/docs",
    },
)