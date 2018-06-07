# # import click

# # @click.group()
# # def authenticate():
# #   click.echo('Enter your dataspine credentials:')
# #   pass

# # @click.group()
# # def main():
# #   pass

# # @authenticate.command()
# # @click.option('--email',
# #   prompt = 'Email',
# #   help = 'User Email.'
# # )
# # @click.option('--password',
# #   prompt = 'Password',
# #   help = 'User Password.',
# #   hide_input = True,
# # )

# # def login(email, password):
# #   """Simple program that authenticate user"""
# #   # click.echo('Email: %s' % email)
# #   # click.echo('Password: %s' % password)
# #   request = {"email": email, "password": password}
# #   url = 'http://18.188.222.86:3000/api/AppUsers/login'

# #   response = requests.post(url, request)
# #   if (response.status_code == 200):
# #     print('Successfully logged in!')
# #   else:
# #     print('Invalid credentials!')

# #   print (response.json())


# # @authenticate.command()
# # # @main.command()
# # def temp():
# #   url = 'http://localhost:5000/help'

# #   response = requests.get(url).json()
# #   for f in response['functions']:
# #     print f




import json
import click
import requests
import subprocess as _subprocess

BASE_URL = 'http://localhost'
#BASE_URL = 'http://52.22.248.211'
PORT = ':5000'

URL = BASE_URL + PORT

@click.group()
def authenticate():
  print('Enter your dataspine credentials:')
  pass

@authenticate.command()
@click.option('--username', prompt = 'Username', help = 'User Name.')
@click.option('--password', prompt = 'Password', help = 'User Password.', hide_input = True)

def login(username, password):
  """Simple program that authenticate user"""
  request = {
    "username": "zeeazmat",
    "password": "zee123123",
  }
  # request = {
  #   "username": username,
  #   "password": password,
  # }
  url = BASE_URL + '/api/token/'

  response = requests.post(url, request)
  if (response.status_code == 200):
    print('Successfully logged in!')
  else:
    print('Invalid credentials!')

  print (response.json())


@click.group()
def main():
  pass


@main.command()
def help():
  """Help command on main group"""
  url = URL + '/help'

  response = requests.get(url).json()
  for f in response['functions']:
    print (f)


@main.command()
def version():
  """Version command on main group"""
  url = URL + '/version'

  response = requests.get(url).json()
  for i in response:
    print (i, response[i], "\n")


@main.command()
@click.option('--model_name', prompt = 'Model name', help = 'Model Name.')
@click.option('--model_tag', prompt = 'Model tag', help = 'Model Tag.')
@click.option('--model_type', prompt = 'Model type', help = 'Model Type.')
@click.option('--model_path', prompt = 'Model path', help = 'Model Path.')
# @click.option('--model_runtime', prompt = 'Model runtime', help = 'Model runtime.', required = False, default = None)

def buildmodel(model_name, model_tag, model_type, model_path):
  """Build model command on main group"""
  url = URL + '/buildmodel'

  request = {
    'model_tag' : model_tag,
    'model_name': model_name,
    'model_type': model_type,
    'model_path': model_path,
    # 'model_runtime': model_runtime,
  }

  print("Building Dockerfile!\n\n")
  response = requests.post(url, request).json()
  
  if (response['command']):
    process = _subprocess.call(response['command'], shell = True)
  else:
    print("Something went wrong!")


cli_commands = click.CommandCollection(sources = [authenticate, main])

if __name__ == '__main__':
  cli_commands()
