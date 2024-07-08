from setuptools import setup, find_packages

setup(
    name='DataHiveToolKit',
    version='0.1',
    packages=find_packages(),
    author='DataHive',
    author_email='contact@datahive.us',
    description='Common utility functions for Data Hive',
    python_requires='>=3.9',
    install_requires=[
        'google_api_python_client>=2.125.0',
        'protobuf>=5.27.2',
        'slack_sdk>=3.21.3'
    ]
)