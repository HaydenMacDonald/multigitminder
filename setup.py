import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multigitminder-hmd", # Replace with your own username
    version="0.1.0",
    author="Hayden MacDonald",
    author_email="hmd@needleinthehay.ca",
    description="A GitHub Action to log data from multiple repos in a single Beeminder goal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HaydenMacDonald/multigitminder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)