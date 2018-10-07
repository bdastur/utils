from setuptools import setup

with open('README.md') as fhandle:
    long_description = fhandle.read()


setup(
    name='builder',
    version='1.0.5',
    description='Utils.',
    long_description=long_description,
    url="https://github.com/bdastur/utils",
    author="Behzad Dastur",
    author_email="bdastur@gmail.com",
    license='Apache Software License',
    classifier=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],

    keywords='nothing-significant',
    py_modules=['rex']
)

