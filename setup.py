from setuptools import setup, find_packages

setup(
    name='trade_fair_webscraper',
    version='0.1',

    # Description of your project
    description='Webscraper for trade fairs',

    # Long description from README file
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    # Author information
    author='Jonas Zilke',
    author_email='jonas.zilke@gmail.com',

    # License information
    license='MIT',

    # Specify packages to be included in the distribution package
    packages=find_packages(),

    # Specify dependencies of the project
    install_requires=[
        'beautifulsoup4==4.12.3',
        'bs4==0.0.2',
        'lxml==5.2.2',
        'selenium==4.22.0',
        'urllib3==2.2.2',
        'webdriver-manager==4.0.1',
    ],

    # Additional classifiers for your project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)