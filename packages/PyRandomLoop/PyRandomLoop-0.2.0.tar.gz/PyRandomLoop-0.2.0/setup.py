from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
name='PyRandomLoop',
version='0.2.0',
author='Lorenzo Gregoris',
author_email='lorenzo.gregoris@gmail.com',
description='Provides a simulation framework for a random loop model in statistical mechanics, including initialization, simulation, and visualization capabilities.' ,
long_description=long_description,
long_description_content_type = 'text/markdown' ,
packages=find_packages(),
license='MIT',
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.9',
)