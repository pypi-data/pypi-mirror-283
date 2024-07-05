from setuptools import setup, find_packages

setup(
    name='training-sdk',
    version='0.0.1',
    description='A Python SDK for training service.',
    author='Luka',
    author_email='luka@bitdeer.com',
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        'grpcio',
        'pydantic'    
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)