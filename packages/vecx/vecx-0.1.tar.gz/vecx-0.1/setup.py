# myproject/setup.py

from setuptools import setup, find_packages

setup(
    name="vecx",
    version="0.1",
    packages=find_packages(),
    package_data={
        '': ['libvx/*'],  # Include all files in the libvx directory
    },
    install_requires=[
        # List your dependencies here
    ],
    author="LaunchX Labs",
    author_email="vectorx@launchxlabs.ai",
    description="A simple example package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/launchxlabs/vectorx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
