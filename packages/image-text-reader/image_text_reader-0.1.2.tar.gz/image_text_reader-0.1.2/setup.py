from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="image_text_reader",
    version="0.1.2",
    author="barmin15",
    author_email="bokora@lauderalumni.hu",
    description="A library to read text from images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/image_text_reader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pytesseract',
        'Pillow'
    ],
)
