from setuptools import setup, find_packages

setup(
    name="termyui",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'windows-curses',
        'pyfiglet',
        'termcolor',
        'term-image'
    ],
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),

)