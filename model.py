#-*- coding: utf-8 -*-

import os
import ssl
import click
import requests
import subprocess as _subprocess
from urllib.request import urlopen
import os.path
from utils.constants import API_URL_BASE


@click.group()
def model():
    """The family commands to work with model"""
    pass


@model.command()
@click.option('--model-name', prompt='Model name', help='Model Name.')
@click.option('--model-tag', prompt='Model tag', help='Model Tag.')
@click.option('--model-type', prompt='Model type', help='Model Type.')
@click.option('--model-path', prompt='Model path', help='Model Path.')
# @click.option('--model_runtime', prompt = 'Model runtime', help = 'Model runtime.', required = False, default = None)
def build(model_name, model_tag, model_type, model_path):
    """Build model command on main group"""

    url = API_URL_BASE + '/buildmodel'
    directory = _subprocess.call('pwd', shell=True)
    request = {
        'model_tag': model_tag,
        'model_name': model_name,
        'model_type': model_type,
        'model_path': model_path,
        # 'model_runtime': model_runtime,
    }

    print("Building Dockerfile!\n\n")
    response = requests.post(url, request).json()
    build_coordinates = response['build_coordinates']

    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars

    fileContent = urlopen(response['dockerFileUrl'], context=gcontext).read().decode('utf-8')
    basePath = os.path.join(os.path.expanduser(model_path))
    filePath = os.path.join(basePath, response['dockerFileName'])

    f = open(filePath, 'w')
    f.write(fileContent)
    f.close()

    cmd = 'docker build %s -f %s %s' % (build_coordinates, filePath, basePath)
    process = _subprocess.call(cmd, shell=True)
    #  if (response['command']):
    #    print(response['command'])
    #    process = _subprocess.call(response['command'], shell = True)
    #  else:
    #    print("Something went wrong!")
    # print(response)


@model.command()
@click.option('--model-name', prompt='Model name', help='Model Name.')
@click.option('--model-tag', prompt='Model tag', help='Model Tag.')
def push(model_name, model_tag):
    """Push model to registry"""
    url = API_URL_BASE + '/modelpush'
    request = {
        'model_tag': model_tag,
        'model_name': model_name,
        # 'model_runtime': model_runtime,
    }
    response = requests.post(url, request).json()
    registry_coordinates = response['registry_coordinates']
    cmd = 'docker push %s' % registry_coordinates
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)


@model.command()
@click.option('--model-name', prompt='Model name', help='Model Name.')
@click.option('--model-tag', prompt='Model tag', help='Model Tag.')
def pull(model_name, model_tag):
    """Fetch model from registry"""
    url = API_URL_BASE + '/modelpull'
    request = {
        'model_name': model_name,
        'model_tag': model_tag,
    }

    response = requests.post(url, request).json()
    pull_coordinates = response['pull_coordinates']
    cmd = 'docker pull %s' % pull_coordinates
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)
