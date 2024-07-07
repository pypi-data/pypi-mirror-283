# setup.py
from setuptools import setup, find_packages

setup(
    name='function_comment',
    version='0.1.0',
    author='Rifat Anwar',
    author_email='rifatanwarrobin@gmail.com',
    description='A library to comment out functions using decorators',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RifatRobin/function_comment',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'dev': ['pytest','unittest'],
    },
)
