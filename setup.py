#!/usr/bin/env python3
# coding : utf-8
from setuptools import setup
import nlpir

dependencies = [
]
setup(
    name='NLPIR-python',
    version=nlpir.__version__,
    packages=['nlpir'],
    url='',
    license='',
    author='yangyaofei, LingJoin Co.,Ltd.',
    author_email='yangyaofei@gmail.com',
    description='',
    python_requires='>=3.6',
    install_requires=dependencies,
    include_package_data=True,
    package_data={'nlpir': ['Data/*.*', 'Data/*/*', 'libs/*']},
    keywords=['nlpir', 'nlp', 'Chinese word segmentation', 'ictclas', 'CWS'],
    test_suite='tests',
    platforms=[
        'win32',
        'win64',
        'linux32',
        'linux64'
        'darwin',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
