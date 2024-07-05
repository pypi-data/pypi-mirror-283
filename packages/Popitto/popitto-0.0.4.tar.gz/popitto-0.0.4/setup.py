from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Basic Pop-It package'

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
LONG_DESCRIPTION = 'A package containing the framework of the traditional Pop-It game'

# Setting up
setup(
    name="Popitto",
    version=VERSION,
    author="Dragjon",
    author_email="<magiciandragjon@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'game', 'board', 'boardgame'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)