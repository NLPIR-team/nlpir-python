#!/usr/bin/env python3
# coding : utf-8
from setuptools import setup, find_packages
import nlpir

with open("README.md", encoding="utf-8") as f:
    readme = f.read()
dependencies = [
    'requests',
]
setup(
    name='nlpir-python',
    version=nlpir.__version__,
    packages=find_packages(),
    url='',
    license='MIT',
    author='yangyaofei, LingJoin Co.,Ltd.',
    author_email='yangyaofei@gmail.com',
    description='NLPIR-python A python wrapper and toolkit for NLPIR',
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    install_requires=dependencies,
    include_package_data=True,
    package_data={'nlpir': ['Data/*.*', 'Data/*/*', 'Data/Sentiment/Data/*', 'Data/Sentiment/Data/*/*', 'lib/*']},
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
    entry_points={
        'console_scripts': [
            'nlpir_update = nlpir.tools:update_license'
        ]
    }
)
