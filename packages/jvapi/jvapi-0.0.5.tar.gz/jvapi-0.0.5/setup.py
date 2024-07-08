from setuptools import setup, find_packages

setup(
    name='jvapi',
    version='0.0.5',
    author='Gye Wong',
    description='A Python package for XYZ',
    long_description='Detailed description of jvapi package.',
    long_description_content_type='text/plain',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
