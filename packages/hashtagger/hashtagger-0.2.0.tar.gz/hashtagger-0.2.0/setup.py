from setuptools import setup, find_packages
import os

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  'Programming Language :: Python :: 3.9',
  'Programming Language :: Python :: 3.10',
  'Programming Language :: Python :: 3.11',
]

# Get the long description from the README and CHANGELOG files
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'CHANGELOG.txt'), encoding='utf-8') as f:
    changelog = f.read()

setup(
  name='hashtagger',
  version='0.2.0',
  description='A hashtag generator using TensorFlow and NLTK',
  long_description=long_description + '\n\n' + changelog,
  long_description_content_type='text/x-rst',
  url='',  # Replace with your GitHub repository URL
  author='Meet Jethwa',
  author_email='meetjethwa3@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='tagger tensorflow nltk',
  packages=find_packages(),
  install_requires=[
        'opencv-python',
        'numpy',
        'tensorflow',
        'nltk',
    ],
  include_package_data=True,
  package_data={
    # If you have any package data to include, specify here
  },
)
