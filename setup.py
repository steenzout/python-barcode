# -*- coding: utf-8 -*-

import sys

import pip
import semver

if 10 >= semver.parse(pip.__version__)['major']:
    import pip._internal.download as pip_download
    from pip._internal.req import parse_requirements
else:
    import pip.download as pip_download
    from pip.req import parse_requirements

from setuptools import setup, find_packages

exec(open('steenzout/barcode/metadata.py').read())

PREFIX = 'py%s%s' % (sys.version_info.major, sys.version_info.minor)


def requirements(requirements_file):
    """Return package mentioned in the given file.

    Args:
        requirements_file (str): path to the requirements file to be parsed.

    Returns:
        (list): 3rd-party package dependencies contained in the file.
    """
    return [
        str(pkg.req) for pkg in parse_requirements(
            requirements_file, session=pip_download.PipSession())]


setup(
    name=__project__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    version=__version__,
    maintainer=__maintainer__,
    maintainer_email=__maintainer_email__,
    url=__url__,
    namespace_packages=['steenzout'],
    packages=find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests')),
    package_data={
        '': [
            'LICENSE', 'NOTICE.md', 'README.md'],
        'steenzout.barcode': [
            'fonts/*']
    },
    classifiers=__classifiers__,
    install_requires=requirements('requirements.txt'),
    tests_require=requirements('requirements-test.txt'),
    license=__license__,
    extras_require={
        'cli': requirements('requirements-extra-cli.txt'),
        'image': requirements('requirements-extra-image.txt'),
    },
    entry_points={
        'console_scripts':
            ['%s-barcode = steenzout.barcode.cli:cli' % PREFIX]
    }
)
