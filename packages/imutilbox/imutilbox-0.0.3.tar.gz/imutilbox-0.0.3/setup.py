from setuptools import setup, find_packages
import os


with open(os.path.join(os.path.dirname(__file__), 'imutilbox', '__init__.py'), encoding='utf-8') as fh:
    for line in fh:
        if line.startswith('__version__'):
            exec(line)
            break


install_requirements = []
with open('requirements.txt') as fh:
    install_requirements = fh.read().splitlines()


setup(
    name        = 'imutilbox',
    version     = __version__,
    description = 'Image Util Box',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
    keywords     = 'image processing',
    author       = 'Jianqiang Sun',
    author_email = 'sun@bitdessin.dev',
    url          = 'https://github.com/bitdessin/imutilbox',
    license      = 'MIT',
    packages     = find_packages(),
    include_package_data = True,
    zip_safe = True,
    long_description = 'Just a simple util for processing images',
    install_requires = install_requirements,
)
