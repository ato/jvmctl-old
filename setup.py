try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'JVM control tool',
    'author': 'Alex Osborne',
    'url': 'https://github.com/ato/jvmctl',
    'download_url': 'https://github.com/ato/jvmctl/tarball/master',
    'author_email': 'ato@meshy.org',
    'version': '0.1.0',
    'install_requires': ['nose'],
    'packages': ['jvmctl'],
    'scripts': [],
    'name': 'jvmctl'
}

setup(**config)
