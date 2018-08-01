from setuptools import setup

setup(
  name='Dataspine Client CLI',
  version='1.0',
  packages=['utils'],
  py_modules=['cli'],
  include_package_data=True,
  install_requires=[ 'click' ],
  entry_points='''
    [console_scripts]
    ds=cli:cli_commands
  ''',
)
