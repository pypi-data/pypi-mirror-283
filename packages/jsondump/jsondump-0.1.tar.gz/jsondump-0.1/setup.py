from setuptools import setup, find_packages

setup(
    name='jsondump',
    version='0.1',
    description="Serialize a object including it's function into a JSON.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jack Watson',
    author_email='jackp.watson888@outlook.com',
    url='https://github.com/devguru008/jsondump',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        # Add dependencies here.
    ],
    extra_requires={
        'dev': [
            'twine'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='json serialize dumps loads unserialize',
    python_requires='>=3.6',
)