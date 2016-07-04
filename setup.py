import os

from setuptools import setup, find_packages

def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

def requirements():
    requirements_list = []

    with open('requirements.txt') as requirements:
        for install in requirements:
            requirements_list.append(install.strip())
    return requirements_list

setup(name='nlp',
      version="1.0",
      description='Python library for natural language processing',
      keywords='python natural language tag',
      url='git@devscm.schibsted.com.br:pedro.lira/nlp.git',
      author='OLX Inc.',
      author_email="dev.scm@olxbr.com",
      license='MIT',
      install_requires=requirements(),
      packages=find_packages(exclude=['tests*']),
      #scripts=['script.py'],
      #data_files=[('config', ['config/simple.cfg'])],
      zip_safe=False,
      include_package_data=True,
      classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Intended Audience :: Developers',
              'Operating System :: OS Independent',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7'
      ]
)
