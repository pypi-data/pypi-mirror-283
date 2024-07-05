from setuptools import setup, find_packages

setup(
    name='training-sdk',
    version='0.0.2',
    description='A Python SDK for training service.',
    author='Luka',
    author_email='luka@bitdeer.com',
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        'grpcio',
        'pydantic'
        'protoc-gen-openapiv2'
        'protobuf'
        'googleapis-common-protos'    
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)