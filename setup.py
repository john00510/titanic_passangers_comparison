import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="titanic_passangers_comparison-yuri0051",
    version="0.0.1",
    author="Yuri",
    author_email="example@email.com",
    description="A dataset comparison package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/john00510/titanic_passangers_comparison",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)