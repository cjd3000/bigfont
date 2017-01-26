import re
from setuptools import setup

NAME = 'bigfont'
DESC = 'renderer for large ascii fonts'
AUTHOR = 'Christopher Durkin'
AUTHOR_EMAIL = 'cjdurkin@github'
PACKAGE = NAME
PACKAGES = [PACKAGE]

with open(PACKAGE + '/__init__.py', 'r') as fd:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

DEPS = []
URL = 'https://github.com/cjdurkin/bigfont'
DOWNLOAD = URL + '/tarball/v' + VERSION
KEYWORDS = []
LICENSE = "ISC"
CLASSIFIERS = [
    'License :: OSI Approved :: ISC License (ISCL)',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

if __name__ == '__main__':
    setup(
        name=NAME,
        version=VERSION,
        description=DESC,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        packages=PACKAGES,
        install_requires=DEPS,
        url=URL,
        download_url=DOWNLOAD,
        keywords=KEYWORDS,
        license=LICENSE,
        classifiers=CLASSIFIERS
    )
