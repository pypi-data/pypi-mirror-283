from setuptools import find_packages, setup

setup(
    name="tesdikin",
    version="0.1",
    description="Library Of @V1HyperBot",
    long_description="V1HyperBot",
    long_description_content_type="text/markdown",
    author="dikin",
    author_email="dikin03101999@gmail.com",
    url="https://github.com/HyperDreamX",
    license="MIT",
    install_requires=["pymongo", "pyromod", "pyrogram", "tgcrypto"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
)
