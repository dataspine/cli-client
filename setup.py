from setuptools import setup

setup(
  name='Dataspine-client',
  version='1.0',
  packages=['utils'],
  py_modules=['cli'],
  include_package_data=True,
  install_requires=['click'],
  entry_points='''
    [console_scripts]
    dataspine=cli:cli_commands
  ''',
)
