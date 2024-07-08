# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['satcube']

package_data = \
{'': ['*']}

install_requires = \
['earthengine-api>=0.1.4.0',
 'fastcubo>=0.0.999',
 'matplotlib>=3.7.0',
 'numpy>=1.25.0',
 'pandas>=2.0.0',
 'phicloudmask>=0.0.2',
 'pydantic>=2.8.0',
 'rasterio>=1.2.0',
 'requests>=2.26.0',
 'satalign>=0.0.999',
 'scikit-learn>=1.2.0',
 'segmentation-models-pytorch>=0.2.0',
 'torch>=2.0.0',
 'xarray>=2023.7.0']

setup_kwargs = {
    'name': 'satcube',
    'version': '0.1.0',
    'description': 'A Python package to create cloud-free monthly composites by fusing Landsat and Sentinel-2 data.',
    'long_description': '# satcube\n\n[colab code](https://colab.research.google.com/drive/1)',
    'author': 'Cesar Aybar',
    'author_email': 'fcesar.aybar@uv.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/IPL-UV/satcube',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
