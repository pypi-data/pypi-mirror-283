from setuptools import setup, find_packages

setup(
    name='MoSort',
    version='0.1.1',
    author='Mohammad Eslami',
    author_email='mohamad.slami@gmail.com',
    description='A Python library that provides Bubble Sort, Quick Sort, and Merge Sort algorithms Written by: Mohammad.E Eslami',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mohammades/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
