from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blitz-player",
    version="0.1.1",
    author="BlitzJB",
    author_email="blitz04.dev@gmail.com",
    description="A CLI YouTube Music player",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blitzjb/blitz-player",
    packages=find_packages(),
    install_requires=[
        "ytmusicapi",
        "yt-dlp",
        "python-vlc",
        "appdirs",
    ],
    entry_points={
        "console_scripts": [
            "bp=blitz_player.player:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)