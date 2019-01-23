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
        'data_flow_graph==0.4.1',
        'elasticsearch-query==2.4.0',
        'sql_metadata==1.5.0',
    ],
    extras_require={
        'dev': [
            'coverage==4.5.2',
            'pylint>=1.9.2, <=2.1.1',  # 2.x branch is for Python 3
            'pytest==4.1.1',
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            # reports
            'http_pandora_mediawiki=graphs.http_pandora_mediawiki:main',
            'portability_metrics=graphs.portability_metrics:main',
            'solr=graphs.solr:main',
        ],
    }
)
