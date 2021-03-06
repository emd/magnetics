try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'magnetics',
    'version': '0.1.1',
    'packages': ['magnetics'],
    'install_requires': [
        'nose', 'numpy', 'matplotlib'],  # and T. Osborne `data`; not on PyPI
    'author': 'Evan M. Davis',
    'author_email': 'emd@mit.edu',
    'url': '',
    'description': 'Python tools DIII-D magnetics signals.'
}

setup(**config)
