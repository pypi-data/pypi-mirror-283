from setuptools import setup, find_packages

setup(
    name='bib_extractor', 
    version='0.0.2', 
    packages=find_packages(
        include=['bib_extractor*', 'test']
        ), 
    entry_points={
        'console_scripts': [
            'bib_extractor_cli=core.bib_extractor_cli:main',
        ],
    },
    include_package_data=True,
    author='dpopov',
    author_email='dpopov@tesyan.ru',
    description='Extraction references and check their style',
)
