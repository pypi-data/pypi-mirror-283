from setuptools import setup, find_packages

setup(
    name='training-sdk',
    version='0.0.5',
    description='A Python SDK for training service.',
    author='Luka',
    author_email='luka@bitdeer.com',
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        'grpcio==1.64.1',
        'protobuf==5.27.2',
        'protoc_gen_openapiv2==0.0.1',
        'pydantic==2.8.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)