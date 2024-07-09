# nxdtest | pythonic package setup
from setuptools import setup, find_packages

setup(
    name        = 'nxdtest',
    version     = '0.0.1',
    description = 'Tox-like tool to run tests for a project under Nexedi testing infrastructure',
    url         = 'https://lab.nexedi.com/nexedi/nxdtest',
    license     = 'GPLv3+ with wide exception for FOSS',
    author      = 'Nexedi',
    author_email= 'kirr@nexedi.com',

    keywords    = 'Nexedi testing infrastructure tool tox',

    packages    = find_packages(),
    install_requires = ['erp5.util', 'six', 'pygolang >= 0.1', 'psutil', 'python-prctl'],
    extras_require = {
                   'test': ['pytest', 'pytest-mock', 'pytest-timeout', 'setproctitle'],
    },

    entry_points= {'console_scripts': ['nxdtest = nxdtest:main']},

    classifiers = [_.strip() for _ in """\
        Development Status :: 3 - Alpha
        Intended Audience :: Developers
        Topic :: Utilities\
    """.splitlines()]
)
