from setuptools import setup, find_packages

setup(
    name="fold_resize_images",
    version='v1.0.4',
    description="A simple tool to resize images in a directory.",
    author="Tadiello Sébastien",
    author_email="sebastientadiello@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Pillow"
    ],
    entry_points={
        'console_scripts': [
            'fold-resize-images=src.fold_resize_images:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
