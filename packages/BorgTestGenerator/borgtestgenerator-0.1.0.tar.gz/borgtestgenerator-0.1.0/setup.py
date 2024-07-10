# setup.py

from setuptools import setup, find_packages

setup(
    name='BorgTestGenerator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['openai'],
    author='Ton Nom',
    author_email='ton.email@example.com',
    description='Librairie pour générer des tests unitaires à partir de scripts Python en utilisant OpenAI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tonrepo/BorgTestGenerator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
