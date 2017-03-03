from setuptools import setup
from setuptools import find_packages

setup(name="jgstrings",
      version="0.1",
      description="A collection of general string algorithms",
      author="Jun Tan",
      author_email="jforce716@gmail.com",
      license="MIT",
      packages=find_packages(exclude=['tests']),
      test_suite="nose.collector",
      tests_require=[
          "nose"
      ])
      
