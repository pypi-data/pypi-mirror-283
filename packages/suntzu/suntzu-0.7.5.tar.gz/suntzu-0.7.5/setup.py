#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

# with open('CONTRIBUTING.md') as contributing_file:
#     contributing = contributing_file.read()

with open("requirements_dev.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()


test_requirements = [""]

setup(
    author="Igor Coimbra Carvalheira",
    author_email='igorccarvalheira111@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    description="SunTzu is a Data Science Python Library that simplifies data tasks, empowering users with robust data science solutions for faster, meaningful analysis. ",
    entry_points={
        'console_scripts': [
            'suntzu=suntzu.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='suntzu, datascience, data science',
    name='suntzu',
    packages=find_packages(include=['suntzu', 'suntzu.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Abigor111/suntzu',
    version='0.7.5',
    zip_safe=False,
)