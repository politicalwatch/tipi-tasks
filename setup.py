from setuptools import setup, find_packages

setup(
    name='tipi-tasks',
    version='1.0.0',
    description='TIPI Alerts',
    url='https://github.com/politicalwatch/tipi-tasks',
    author='danigm',
    packages=find_packages(),
    install_requires=[
        'celery',
        'redis',
        'mongoengine',
        'sparkpost',
        'jinja2',
    ],
)
