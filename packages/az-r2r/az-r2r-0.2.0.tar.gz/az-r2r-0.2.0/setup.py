from setuptools import setup, find_packages

setup(
    name='az-r2r',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[],  # add any dependencies here
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple package to parse strings and count characters, words, special characters, and numbers.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)