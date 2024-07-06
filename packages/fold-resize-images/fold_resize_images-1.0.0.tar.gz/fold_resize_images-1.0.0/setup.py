from setuptools import setup, find_packages

setup(
    name="fold_resize_images",
    version="0.1.0",
    description="A simple tool to resize images in a directory.",
    author="Tadiello Sébastien",
    author_email="sebastientadiello@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
