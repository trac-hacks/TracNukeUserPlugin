from setuptools import find_packages, setup

# name can be any name.  This name will be used to create .egg file.
# name that is used in packages is the one that is used in the trac.ini file.
# use package name as entry_points

import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='TracNukeUserPlugin',
    version='0.2.2',
    author='Paul Winkler',
    author_email='slinkp@gmail.com',
    description = "trac-admin command to remove the specified Trac user and all tickets they created",
    long_description=read('README.txt'),
    license = """BSD""",
    url = "https://github.com/slinkp/TracNukeUserPlugin",
    packages = find_packages(exclude=['*.tests*']),
    install_requires = [
        'Trac>=0.12',
        'TracSpamFilter',
    ],
    entry_points = """
        [trac.plugins]
        nukeuser = nukeuserplugin
    """,
   classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Framework :: Trac',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2',
   ],
)
