import os
from setuptools import find_packages
from setuptools import setup

import os
from setuptools import find_packages, setup

def _read_reqs(path: str) -> list[str]:
    if not os.path.isfile(path):
        return []
    with open(path) as f:
        return [x.strip() for x in f.readlines() if x.strip() and not x.startswith('#') and 'git+' not in x]

requirements = _read_reqs('requirements.txt')
requirements_dev = _read_reqs('requirements_dev.txt')

setup(
    name='bricklawyer',
    version='0.0.1',
    description='Project Description',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={'dev': requirements_dev},
    test_suite='tests',
    # include_package_data: to install data from MANIFEST.in
    include_package_data=True,
    # scripts=['scripts/bricklawyer-run'],
    zip_safe=False,
)
