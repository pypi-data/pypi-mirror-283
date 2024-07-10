# setup.py
from setuptools import setup, find_packages

setup(
    name='robotframework-restbridge',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'robotframework',
    ],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
    author='Your Name',
    author_email='PyPI.Releases@viadee.de',
    description='This is a robotframework keyword library to allow single command execution via HTTP.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/raffelino/robotframework-restbridge',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
