import os
from os import path
from setuptools import setup, find_packages

# for pip >= 10
try:
    from pip._internal.req import parse_requirements
# for pip <= 9.0.3
except ImportError:
    from pip.req import parse_requirements


REQUIREMENTS_PATH = path.join(path.dirname(__file__), 'requirements.txt')
install_reqs = parse_requirements(REQUIREMENTS_PATH, session='')
reqs = [str(ir.req) for ir in install_reqs if ir]
setup(
    name='cody',
    version='0.0.1',
    install_requires=reqs,
    packages=['cody'],
    long_description=f'\n{os.environ.get("VERSION")}',
    include_package_data=True,
)
