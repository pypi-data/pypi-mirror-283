# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="fosforml",
    package_dir={"fosforml":"fosforml"},
    version="1.0.2",
    description="REST API client for Fosfor AI",
    url="https://gitlab.fosfor.com/fosfor-decision-cloud/intelligence/mosaic-ai-client.git",
    author="Rakesh Gadiparthi",
    author_email="rakesh.gadiparthi@fosfor.com",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cloudpickle==2.2.1",
        "requests-toolbelt==1.0.0",
        "shutils==0.1.0",
        "PyYAML==6.0.1",
        "mosaic-utils",
        "urllib3==2.2.1",
        'numpy==1.26.4; python_version>"3.8"',
        'numpy==1.24.4; python_version<="3.8"',
        'snowflake-ml-python==1.5.0; python_version<="3.9"',
        'snowflake-ml-python==1.5.1; python_version=="3.10"',
        'snowflake-ml-python==1.5.3; python_version>="3.11"',
        'scikit-learn==1.3.2'
    ]
)
 
