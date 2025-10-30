"""Setup script for cdek-sdk-2 package."""

from setuptools import setup

# Читаем содержимое README
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Python SDK для работы с API СДЭК версии 2.0"

setup(
    name="cdek",
    version="2.0.0",
    description="Python SDK для работы с API СДЭК версии 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CDEK Python SDK",
    author_email="support@cdek.ru",
    url="https://github.com/cdek/sdk-python",
    packages=[
        "cdek",
        "cdek.requests",
        "cdek.responses",
        "cdek.exceptions",
        "cdek.mixin",
    ],
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    include_package_data=True,
    zip_safe=False,
)

