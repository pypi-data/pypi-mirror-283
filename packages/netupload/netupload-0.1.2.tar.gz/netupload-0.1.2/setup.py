from setuptools import setup, find_packages

setup(
    name="netupload",
    author="Zach Grimaldi",
    version="0.1.2",
    description="Simple upload server for local network file transfers.",
    long_description=open("README.md").read(),
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
