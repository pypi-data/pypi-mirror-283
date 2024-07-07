from setuptools import setup, find_packages

setup(
    name='puzzlecreator',
    version='1.1.4',
    packages=find_packages(),
    install_requires=[],
    author='frank vitetta',
    author_email='frank@orchidbox.com',
    description='A package for creating crossword puzzles by Orchid Box.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://orchidbox.com/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
