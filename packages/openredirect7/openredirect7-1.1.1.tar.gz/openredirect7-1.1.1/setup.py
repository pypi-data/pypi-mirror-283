from setuptools import setup, find_packages

VERSION = '1.1.1'
DESCRIPTION = 'A Tool to find an Easy Bounty - Open Redirect'
LONG_DESCRIPTION = 'This is a tool used by several security researchers to find Open Redirect.'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openredirect7",
    version=VERSION,
    author="@yashwanth",
    author_email="yashwanthrvy7@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['urllib3', 'requests', 'argparse'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
