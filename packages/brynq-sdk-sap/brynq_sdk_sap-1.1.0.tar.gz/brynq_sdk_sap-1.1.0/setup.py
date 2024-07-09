from setuptools import setup

setup(
    name='brynq_sdk_sap',
    version='1.1.0',
    description='SAP wrapper from BrynQ',
    long_description='SAP wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.sap"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'requests>=2,<=3',
        'requests_oauthlib>=1,<=2',
        'oauthlib>=3,<=4',
        'pandas_read_xml>=0,<1',
        'pandas>=1,<3',
        'pyarrow>=10'
    ],
    zip_safe=False,
)
