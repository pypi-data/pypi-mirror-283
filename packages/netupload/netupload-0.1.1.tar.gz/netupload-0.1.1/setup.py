from setuptools import setup, find_packages

setup(
    name="netupload",
    author="Zach Grimaldi",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "Flask",
    ],
    entry_points={
        "console_scripts": [
            "netupload=src.app:run_server",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
