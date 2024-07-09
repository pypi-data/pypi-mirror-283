# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastcubo']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.0.0', 'utm>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'fastcubo',
    'version': '0.0.9999',
    'description': '🏎💨vroom vroom - data downloader',
    'long_description': '# FastCubo\n\nA simple API for `ee.data.pixels` inspired by [cubo](https://github.com/ESDS-Leipzig/cubo), designed for creating and managing data cubes up to 10 times faster.\n\n## Installation\n\nInstall the latest version from PyPI:\n\n```bash\npip install fastcubo\n```\n\n## How to use\n\n\nDownload a ee.Image\n\n```python\nimport ee\nimport fastcubo\n\nee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")\n\n\ntable = fastcubo.query_getPixels_image(\n    points=[(-76.5, -9.5), (-76.5, -10.5), (-77.5, -10.5)],\n    collection="NASA/NASADEM_HGT/001",\n    bands=["elevation"],\n    edge_size=128,\n    resolution=90\n)\n\nfastcubo.getPixels(table, nworkers=4, output_path="demo1")\n```\n\nDownload a ee.ImageCollection\n\n```python\nimport fastcubo\nimport ee\n\nee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")\n\ntable = fastcubo.query_getPixels_imagecollection(\n    point=(51.079225, 10.452173),\n    collection="COPERNICUS/S2_HARMONIZED", # Id of the GEE collection\n    bands=["B4","B3","B2"], # Bands to retrieve\n    data_range=["2016-06-01", "2017-07-01"], # Date range of the data\n    edge_size=128, # Edge size of the cube (px)\n    resolution=10, # Pixel size of the cube (m)\n)\nfastcubo.getPixels(table, nworkers=4, output_path="demo2")\n```\n\n\nDownload a ee.Image Compute Pixels\n\n```python\nimport fastcubo\nimport ee\n\nee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")\n\ntable = fastcubo.query_computePixels_image(\n    points=[(-76.5, -9.5), (-76.5, -10.5), (-77.5, -10.5)],\n    expression=ee.Image("NASA/NASADEM_HGT/001").divide(1000),\n    bands=["elevation"],\n    edge_size=128,\n    resolution=90\n)\nfastcubo.computePixels(table, nworkers=4, output_path="demo3")\n```',
    'author': 'Cesar Aybar',
    'author_email': 'fcesar.aybar@uv.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/csaybar/fastcubo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
