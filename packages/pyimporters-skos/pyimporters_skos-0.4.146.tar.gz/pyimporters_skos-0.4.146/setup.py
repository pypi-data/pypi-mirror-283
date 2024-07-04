#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pyimporters_skos']

package_data = \
{'': ['*']}

install_requires = \
['pyimporters_plugins>=0.4.0,<0.5.0', 'rdflib', 'rdflib-jsonld']

entry_points = \
{'pyimporters.plugins': ['skos = pyimporters_skos.skos:SKOSKnowledgeParser']}

setup(name='pyimporters-skos',
      version='0.4.146',
      description='Sherpa knowledge import plugins',
      author='Olivier Terrier',
      author_email='olivier.terrier@kairntech.com',
      url='https://kairntech.com/',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      entry_points=entry_points,
      python_requires='>=3.8',
     )
