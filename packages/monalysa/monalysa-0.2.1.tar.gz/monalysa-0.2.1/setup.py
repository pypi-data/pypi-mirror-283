# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monalysa',
 'monalysa.preprocess',
 'monalysa.quality',
 'monalysa.tests',
 'monalysa.ulfunc']

package_data = \
{'': ['*'], 'monalysa': ['.idea/*', '.idea/inspectionProfiles/*']}

setup_kwargs = {
    'name': 'monalysa',
    'version': '0.2.1',
    'description': 'A unified library for quantitative movement analysis.',
    'long_description': '# <span style="color:#555"><span style="color:#A62B17">**Mo**</span>vement  A<span style="color:#A62B17">**nalys**</span>is Libr<span style="color:#A62B17">**a**</span>ry (Monalysa)</span>\n\nMonalysa, _aka_ <u>**Mo**</u>vement a<u>**nalys**</u>is libr<u>**a**</u>ry, is a unified python library for the quantitative analysis of sensorimotor behavior. Monalysa provides a set of data structures, functions, and classes for representing, analyzing, and visualizing movement-related data from different technologies (motion capture, inertial measurement units, robots, force/torque sensors, force plates, etc.).\n\n## Purpose of the library\nIn the spirit of open science, the monalysa library provides open-source code for a set of commonly used methods, measures, and tools for analyzing movement data. Such a library can be a step towards the standardization of procedures used for movement analysis.\n\n## Who is this library for?\nThis library is aimed at students, researchers, clinicians and industry professionals working with movement data.\n\n## Installing Monalysa \nMonalysa is available through PyPI and can be easily installed using the following pip command.\n```console\n(.venv) $ pip install monalysa  \n````\n\n## Read the Documentation\nYou can find the documentation for the Monalysa library at [https://monalysa.readthedocs.io/en/latest/](https://monalysa.readthedocs.io/en/latest/).\n\n## Contributors\nSivakumar Balasubramanian, Tanya Subash, Alejandro Melendez-Calderon, Camila Shirota.',
    'author': 'Sivakumar Balasubramanian (Siva)',
    'author_email': 'siva82kb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/siva82kb/monalysa',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
