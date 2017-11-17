"""
Setup application info.
"""
from setuptools import setup

setup(name='mobicomp',
      version='1.0',
      description='OpenShift App',
      author='Marcus Hunt',
      author_email='mrhapi@outlook.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.12.2',
                        'requests>=2.10.0',
                        'click>=6.6',
                        'itsdangerous==0.24',
                        'Jinja2==2.6',
                        'Werkzeug==0.12.2ß']
     )
