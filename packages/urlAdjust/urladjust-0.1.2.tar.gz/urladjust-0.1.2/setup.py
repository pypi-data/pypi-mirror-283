from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='urlAdjust',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[],
    description='UrlAdjust is a Python package that help developer generate get http request url with template and adjustment info. It aims to simplify the url generation process for get http request url. ',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Use 'text/x-rst' if you use reStructuredText
    author='Yu Xing',
    author_email='f0x.sideproject@gmail.com',
    url='https://github.com/F-0-X/UrlAdjust',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)