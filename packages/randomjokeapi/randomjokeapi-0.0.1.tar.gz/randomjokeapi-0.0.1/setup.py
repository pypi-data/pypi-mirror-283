import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="randomjokeapi",
    version="0.0.1",
    author="Asrin Vakili",
    author_email="asrin_vakili@yahoo.com",
    description="get current temperature from provider",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asrinvakili/RndomJokeAPI",
    project_urls={
        "Author": "https://github.com/asrinvakili",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "requests"
    ]
)