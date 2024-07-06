# nxdbom | pythonic package setup
from setuptools import setup, find_packages

setup(
    name        = 'nxdbom',
    version     = '0.0.1',
    description = 'Tool to generate bill of material for Nexedi-built software',
    url         = 'https://lab.nexedi.com/nexedi/nxd-bom',
    license     = 'GPLv3+ with wide exception for FOSS',
    author      = 'Nexedi',
    author_email= 'kirr@nexedi.com',

    keywords    = 'Nexedi software build BOM',

    packages    = find_packages(),
    extras_require = {
                   'test': ['pytest'],
    },

    entry_points= {'console_scripts': ['nxdbom = nxdbom:main']},

    classifiers = [_.strip() for _ in """\
        Development Status :: 3 - Alpha
        Intended Audience :: Developers
        Topic :: Utilities\
    """.splitlines()]
)
