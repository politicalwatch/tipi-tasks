from setuptools import setup, find_packages

setup(
    name='tipi-tasks',
    version='1.0.0',
    description='TIPI Data',
    url='https://github.com/politicalwatch/tipi-tasks',
    author='danigm',
    packages=find_packages(),
    install_requires=[
        'tipi-data @ https://github.com/politicalwatch/tipi-data@master'
        'git+https://github.com/politicalwatch/tipi-data.git',
        'amqp==2.3.2',
        'billiard==3.5.0.5',
        'celery[redis]==4.2.1',
        'certifi==2018.11.29',
        'chardet==3.0.4',
        'idna==2.7',
        'jinja2>=2.10.1',
        'kombu==4.2.1',
        'markupsafe==1.1.0',
        'mongoengine==0.16.2',
        'pymongo==3.7.2',
        'python-pcre==0.7',
        'pytz==2018.7',
        'redis==2.10.6',
        'requests==2.20.1',
        'sentry-sdk[celery]==0.14.1',
        'six==1.11.0',
        'sparkpost==1.3.6',
        'urllib3==1.24.2',
        'vine==1.1.4',
    ],
)
