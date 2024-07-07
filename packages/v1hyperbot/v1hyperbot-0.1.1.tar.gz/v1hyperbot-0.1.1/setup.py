from setuptools import find_packages, setup

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="v1hyperbot",
    version="0.1.1",
    description="Library of @V1HyperBot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="admin",
    author_email="admin@V1HyperBot.com",
    url="https://t.me/NorSodikin",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
)
