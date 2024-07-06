from setuptools import setup, find_packages

setup(
    name="library-bot-pp",
    version="0.3",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'p!c=librarypp.scripts.create_file:create_file',
        ],
    },
    author="P",
    author_email="parepare2154@gmail.com",
    description="A library that creates a Python bot",
    url="https://ppbot.web.app/mylibrary",
)
