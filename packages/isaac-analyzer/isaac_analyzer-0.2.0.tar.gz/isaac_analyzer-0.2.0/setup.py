from setuptools import setup, find_packages

setup(
    name="isaac-analyzer",
    version="0.2.0",
    packages=find_packages(),
    package_data={"isaac_analyzer": ["resources/*"]},
    install_requires=[
        "pyyaml",
        "tabulate",
        "jsonschema",
        "matplotlib",
        "numpy",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "isaac-analyzer=isaac_analyzer.cli:main",
        ],
    },
    author="Supporterino",
    author_email="lars@roth-kl.de",
    description="A CLI application to analyze isaac runs documented in YAML",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://git.roth-kl.de/isaac/isaac-analyzer",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
