# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deepdiagnostics',
 'deepdiagnostics.client',
 'deepdiagnostics.data',
 'deepdiagnostics.metrics',
 'deepdiagnostics.models',
 'deepdiagnostics.plots',
 'deepdiagnostics.utils']

package_data = \
{'': ['*']}

install_requires = \
['deprecation>=2.1.0,<3.0.0',
 'getdist>=1.4.7,<2.0.0',
 'h5py>=3.10.0,<4.0.0',
 'matplotlib>=3.8.3,<4.0.0',
 'numpy>=1.18.5,<1.26.0',
 'pyarrow>=15.0.0,<16.0.0',
 'sbi>=0.22.0,<0.23.0',
 'scipy>=1.6.0,<1.12.0',
 'tarp>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['diagnose = deepdiagnostics.client.client:main']}

setup_kwargs = {
    'name': 'deepdiagnostics',
    'version': '1.0.0',
    'description': 'a package for diagnosing posterior quality from inference methods',
    'long_description': 'None',
    'author': 'Becky Nevin',
    'author_email': 'rnevin@fnal.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
