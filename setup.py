from setuptools import setup, find_packages

setup(
    name="tipi-tasks",
    version="1.0.0",
    description="TIPI Data",
    url="https://github.com/politicalwatch/tipi-tasks",
    author="danigm",
    packages=find_packages(),
    install_requires=[
        "tipi-data @ git+https://github.com/politicalwatch/tipi-data.git",
        "celery[redis]==4.4.7",
        "certifi==2024.6.2",
        "chardet==3.0.4",
        "idna==3.7",
        "jinja2>=2.11.3",
        "markupsafe==1.1.1",
        "mongoengine==0.28.2",
        "pymongo==4.7.2",
        "python-pcre==0.7",
        "pytz==2024.1",
        "requests==2.32.3",
        "six==1.12.0",
        "sparkpost==1.3.10",
        "urllib3==1.26.18",
    ],
)
