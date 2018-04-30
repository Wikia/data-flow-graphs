from setuptools import setup

from graphs import __version__

setup(
    name='graphs',
    version=__version__,
    description='An open repository with scripts used to generate data-flow-graphs',
    url='https://github.com/Wikia/data-flow-graphs',
    author='macbre',
    author_email='macbre@wikia-inc.com',
    install_requires=[
        'wikia-common-kibana==2.2.1',
        'data_flow_graph==0.1'
    ],
    extras_require={
        'dev': [
            'coverage==4.5.1',
            'pylint==1.8.2',
            'pytest==3.4.0',
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            # reports
            'http_requests_graph=graphs.http_requests:main',
        ],
    }
)
