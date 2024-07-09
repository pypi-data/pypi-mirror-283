"""
Setup file for the Profit Potion library.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="profit_potion",
    version="0.0.7",  # Asegúrate de actualizar esta versión manualmente
    author="Gabriel Gonzalez",
    author_email="gabrielgonzalezcifuentes@gmail.com",
    description="A magical financial analysis library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gabwill10/profit-potion.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests>=2.32.3",
        "openai>=1.35.3"
    ],
)
