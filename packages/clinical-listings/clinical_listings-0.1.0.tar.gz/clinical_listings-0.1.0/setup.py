from setuptools import setup, find_packages

setup(
    name='clinical_listings',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'sqlalchemy',
        'sas7bdat',
        'reportlab',
        'fpdf',
    ],
    entry_points={
        'console_scripts': [
            'clinical_listings=clinical_listings.__main__:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for creating formatted clinical trial listings.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/clinical_listings',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
