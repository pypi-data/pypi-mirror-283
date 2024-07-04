import setuptools

setuptools.setup(
    name='ficus-pm',
    version='1.0.1',
    author='Aero',
    author_email='aerooneq@yandex.ru',
    description='The modern Process Mining toolkit',
    long_description='The modern Process Mining toolkit',
    long_description_content_type="text/markdown",
    license='private',
    packages=['ficus',
              'ficus.legacy',
              'ficus.legacy.discovery',
              'ficus.legacy.log',
              'ficus.legacy.analysis',
              'ficus.legacy.analysis.patterns',
              'ficus.legacy.analysis.common',
              'ficus.legacy.pipelines',
              'ficus.legacy.pipelines.analysis',
              'ficus.legacy.pipelines.analysis.patterns',
              'ficus.legacy.pipelines.serialization',
              'ficus.legacy.pipelines.discovery',
              'ficus.legacy.pipelines.filtering',
              'ficus.legacy.pipelines.mutations',
              'ficus.legacy.pipelines.contexts',
              'ficus.legacy.pipelines.start',
              'ficus.legacy.mutations',
              'ficus.legacy.filtering',
              'ficus.grpc_pipelines',
              'ficus.grpc_pipelines.models'],
    install_requires=['pm4py==2.7.7',
                      'matplotlib==3.8.0',
                      'matplotlib-inline==0.1.6',
                      'graphviz~=0.20.1',
                      'intervaltree~=3.1.0',
                      'ipython==8.16.1',
                      'numpy~=1.26.0',
                      'pandas==2.1.1',
                      'setuptools==68.2.2',
                      'python-dateutil~=2.8.2',
                      'ipycanvas~=0.13.1',
                      'pytest~=7.4.2',
                      'grpcio==1.59.0',
                      'grpcio-tools==1.59.0',
                      'suffix-tree==0.1.2',
                      'scikit-learn~=1.3.2',
                      'attrs~=23.1.0']
)
