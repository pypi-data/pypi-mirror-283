from setuptools import setup, find_packages
import os

VERSION = '0.0.7'
DESCRIPTION = 'meiya pico ai tools for process data '

setup(
    name="meiya_ai",
    version=VERSION,
    author="yuhan zhangyh",
    author_email="yhanzh0608@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md',encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['pandas', 'datasets'],
    keywords=['python', 'data  process', 'meiyapico ai'],
    data_files=[],
    entry_points={
    'console_scripts': [
        'meiya_ai = meiya_ai.main:main'
    ]
    },
    license="MIT",
    url="https://github.com/amanyara",
    scripts = [],
    # scripts=['meiya_ai/filter/pandas_filter/filter_pandas.py',
    #          "meiya_ai/filter/hashlib_filter/filter_hashlib.py"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux"
    ]
)