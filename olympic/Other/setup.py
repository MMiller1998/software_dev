from setuptools import setup, find_packages

setup(
    name='finger-lakes',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.ccs.neu.edu/CS4500-F21/finger-lakes',
    description='CS4500 Trains Game',
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'xmap = trains.xmap.__main__:main',
            'xvisualize = trains.editor.__main__:main',
            'xlegal = trains.xlegal.__main__:main',
            'xstrategy = trains.xstrategy.__main__:main',
            'xref = trains.xref.__main__:main',
            'xmanager = trains.xmanager.__main__:main',
            'xserver = trains.xserver.__main__:main',
            'xclients = trains.xclients.__main__:main'
        ]
    }
)
