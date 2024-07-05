from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
setup(
    name='kt-ai-iot',
    version='0.3.0',
    author='Rossi',
    author_email='rizzieang@gmail.com',
    description='A library for controlling KT-AI-IOT devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyserial',
        'numpy'
    ],
)