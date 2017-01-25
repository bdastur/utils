from setuptools import setup


setup(
    name='pystatsd',
    version='1.0.0',
    description='Python statsd server.',
    long_description="Python statsd server",
    url="https://github.com/bdastur/utils",
    author="Behzad Dastur",
    author_email="bdastur@gmail.com",
    license='Apache Software License',
    classifier=[
        'Development Status :: 3 - Alpha',
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

    entry_points={
        'console_scripts': [
            'pystats = pystats.stats_server:main'
        ]
    },
    keywords='statsd',
    packages=["pystats"],
    data_files = [('/etc/pystat', ['pystats/etc/pystats/pystat.conf'])],
    install_requires=['kafka-python',
                      'PyYAML']
)
