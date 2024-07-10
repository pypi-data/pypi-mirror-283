from setuptools import setup, find_packages
import yaml


def get_version_from_swagger():
    with open("debiaiServer/swagger.yaml", "r") as f:
        swagger_data = yaml.safe_load(f)
    return swagger_data["info"]["version"]


VERSION = get_version_from_swagger()

setup(
    name="debiai-gui",
    version=VERSION,
    packages=find_packages(include=["debiaiServer", "debiaiServer.*"]),
    include_package_data=True,
    install_requires=[
        "Flask==2.0.3",
        "flask_cors==3.0.8",
        "connexion==2.6.0",
        "requests==2.25.1",
        "swagger-ui-bundle==0.0.5",
        "pandas==1.5.1",
        "scipy==1.9.3",
        "ujson==5.8.0",
        "sklearn==0.0",
        "kafka-python==2.0.2",
        "openapi_spec_validator==0.2.8",
        "PyYAML==6.0",
        "cacheout==0.14.1",
        "termcolor==2.3.0",
        "werkzeug==2.2.2",
    ],
    entry_points={
        "console_scripts": [
            "debiai-gui=debiaiServer.server:run",
        ],
    },
    author="IRT-Systemx",
    author_email="debiai@irt-systemx.fr",
    description="DebiAI easy start module, the standalone version of DebiAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/debiai/DebiAI",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
