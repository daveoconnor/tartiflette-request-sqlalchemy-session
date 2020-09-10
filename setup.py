import setuptools
from os import sys

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name="tartiflette-request-sqlalchemy-session",
    version="0.9.1",
    author="Dave O'Connor",
    author_email="github@dead-pixels.org",
    description="Middleware for the [tartiflette](https://tartiflette.io/) " +
                "GraphQL server implementation to have a SQLAlchemy Session" +
                " generated on each server request which is then injected " +
                "into the resolver context.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daveoconnor/tartiflette-request-sqlalchemy-session",
    packages=setuptools.find_packages(include=[
        'tartiflette_request_sa_session',
    ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        "tartiflette-request-context-hooks>=0.9",
        "SQLAlchemy>=1.3",
    ],
    extras_require={
        "psycopg": ['psycopg2-binary>=2.8'],
    },
    tests_require=[
        "pytest>=6.0",
        "pytest-asyncio>=0.14",
        "pytest-xdist>=1.34",
        "pytest-cov>=2.10",
    ],
    setup_requires=[] + pytest_runner,
)
