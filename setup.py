"""Setup script for cdek package."""

try:
    from setuptools import find_packages, setup
except (
    ModuleNotFoundError
) as exc:  # pragma: no cover - выполняется только при отсутствии зависимости
    raise RuntimeError(
        "Для сборки пакета требуется установить setuptools: pip install setuptools"
    ) from exc

# Читаем содержимое README
try:
    with open("README.md", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Python SDK для работы с API СДЭК версии 2.0"

setup(
    name="cdek",
    version="1.0.1",
    description="Python SDK для работы с API СДЭК версии 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CDEK Python SDK",
    author_email="geomer198@gmail.com",
    url="https://github.com/xxp-odoo-erp/cdek",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.6,<3.0",
        "requests>=2.28.0",
    ],
    include_package_data=True,
    zip_safe=False,
)
