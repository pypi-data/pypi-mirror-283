from setuptools import setup, find_packages

setup(
    name='neyro-api',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'aiohttp'
    ],
    author='Chelik23',
    author_email='workghmail5775@gmail.com',
    description='A Python library for interacting with the Neyro API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)