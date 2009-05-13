from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='concrawl',
      version=version,
      description="Crawl and harvest linked data from Atom feeds",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='Sean Gillies',
      author_email='sean.gillies@gmail.com',
      url='http://concordia.atlantides.org/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'zc.dict',
        'multiprocessing',
        'httplib2'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
