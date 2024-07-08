from setuptools import setup, find_packages

setup(
    name='verify-project-demo',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A sample Python package that generates test code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/verify-project-demo',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
