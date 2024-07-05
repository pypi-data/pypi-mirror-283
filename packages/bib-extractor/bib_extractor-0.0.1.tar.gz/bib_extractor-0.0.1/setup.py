from setuptools import setup, find_packages

setup(
    name='bib_extractor', 
    version='0.0.1', 
    packages=find_packages(exclude=['tmp_dir', '*.pyc', '__pycache__', '.venv']), 
    entry_points={
        'console_scripts': [
            'bib_extractor_cli=core.bib_extractor_cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.json'],
    },
    author='dpopov',
    author_email='dpopov@tesyan.ru',
    description='Extraction references and check their style',
)
