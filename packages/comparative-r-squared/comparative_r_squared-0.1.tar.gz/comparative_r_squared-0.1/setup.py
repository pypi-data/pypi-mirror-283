from setuptools import setup, find_packages

setup(
    name='comparative_r_squared',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scipy',
        'numpy',
        'statsmodels'
    ],
    author='Shashank Ramachandran',
    author_email='sr31@Bu.edu',
    description='Package for calculating Comparative R Squared',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/comparative_r_squared',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
