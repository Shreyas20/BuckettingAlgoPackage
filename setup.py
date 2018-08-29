import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bucketting",
    version="0.0.1",
    author="Shreyas Kulkarni",
    author_email="shreyaskulkarni20@gmail.com",
    description="Converting integer array into categorical buckets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shreyas20/BuckettingAlgoPackage",
    packages=setuptools.find_packages(),
    install_requires=['pandas','numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)

