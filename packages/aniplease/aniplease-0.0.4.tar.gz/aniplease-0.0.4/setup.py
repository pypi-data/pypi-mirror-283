import setuptools

name = "aniplease"
version = "v0.0.4"
author = "EncodePlease Team"
author_email = "encodeplease@proton.me"
lic = "GNU AFFERO aa rha posts GENERAL PUBLIC LICENSE (v3)"
reqs = ["aiohttp", "aiofiles", "asyncio", "requests", "tqdm"]
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description="",
    long_description="# We Don't Know",
    long_description_content_type="text/markdown",
    license=lic,
    packages=setuptools.find_packages(),
    install_requires=reqs,
    classifiers=classifiers,
    python_requires=">=3.6",
)