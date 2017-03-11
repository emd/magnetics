try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'magnetics',
    'version': '0.1',
    'packages': ['magnetics'],
    'install_requires': ['nose', 'random_data'],
    'author': 'Evan M. Davis',
    'author_email': 'emd@mit.edu',
    'url': '',
    'description': 'Python tools DIII-D magnetics signals.'
}

setup(**config)
