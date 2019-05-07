from setuptools import setup, find_packages

setup(
    name='mas',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='ulyanin',
    author_email='ulyanin.da@phystech.edu',
    description='',
    install_requires=[
        'click==6.7',
        'tornado==5.0.2',
        'statsd==3.3.0',
        'requests',
        'cassandra-driver>=3.17.0',
        'aiocassandra>=2.0.1',
        'aioredis'
    ]
)
