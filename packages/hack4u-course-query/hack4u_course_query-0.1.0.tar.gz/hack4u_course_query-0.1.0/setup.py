from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u-course-query",  # Shortened package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",  # Example dependency
    ],
    author="Juan Moncada",
    description="A library for querying Hack4u courses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
    license="MIT",  # Added license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'hack4u-query = your_package.scripts.query:main', # Example entry point
        ],
    },
)
