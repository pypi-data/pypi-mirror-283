# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from MixPage import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="BenMixPage",
    version=__version__,
    author="g1879",
    author_email="g1879@qq.com",
    description="Python based web automation tool. It can control the browser and send and receive data packets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="MixPage",
    url="https://gitee.com/g1879/MixPage",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'lxml',
        'requests',
        'cssselect',
        'DownloadKit>=0.5.3',
        'selenium',
        'tldextract'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.6',
)
