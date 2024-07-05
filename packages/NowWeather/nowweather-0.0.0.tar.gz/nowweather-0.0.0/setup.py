import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NowWeather",
    version="0.0.0",
    author="AiraSato",
    author_email="asato@sciencepark.co.jp",
    description="how to debut a PyPI for chemistry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spc-asato/NowWeather",
    project_urls={
        "Bug Tracker": "https://github.com/spc-asato/NowWeather",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['NowWeather'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'NowWeather = NowWeather:main'
        ]
    },
)
