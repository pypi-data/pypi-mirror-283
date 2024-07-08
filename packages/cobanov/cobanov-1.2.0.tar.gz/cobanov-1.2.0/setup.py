from setuptools import setup, find_packages

setup(
    name="cobanov",
    version="1.2.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cobanov=cobanov.main:main",
        ],
    },
    install_requires=[
        "psutil",
        'pyudev; platform_system=="Linux"',  # Conditional dependency for Linux only
    ],
    author="Mert Cobanov",
    author_email="mertcobanov@gmail.com",
    description="Cobanov command line tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cobanov/cobanov-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
