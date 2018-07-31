#-*- coding: utf-8 -*-

import os
import jwt
import ssl
import time
import json
import click
import requests
import calendar
from functools import wraps
import subprocess as _subprocess
from urllib.request import urlopen
import kubernetes.client as _kubeclient
import kubernetes.config as _kubeconfig
import warnings as _warnings
import yaml
from basicauth import encode
import keyring
from pathlib import Path
import configparser


data = {}
decoded_data = {}
BASE_URL = 'http://localhost'
# BASE_URL = 'http://52.22.248.211'
PORT = ':5000'
URL = BASE_URL + PORT
secret = 'bw$u55&le#a=mm_zths96b!i@0=z7)#c9#k)4!j(q1f9+8^8y0'
current_time = calendar.timegm(time.gmtime())


def valid_token():
    if ('exp' in decoded_data):
        return (current_time < decoded_data['exp'])
    else:
        return False


@click.group()
def authenticate():
    print('Enter your dataspine credentials:')
    pass


@authenticate.command()
def get_encoded_string():
    home = str(Path.home())
    filename_profiles = home + "/.dataspine/userdata"
    config = configparser.ConfigParser()
    config.read(filename_profiles)
    username = config.get('default', 'username')
    account_uuid = config.get('default', 'account-uuid')
    password = keyring.get_password(account_uuid, username)
    encoded_str = encode(username, password)

    return encoded_str


@authenticate.command()
def get_account_uuid():
    home = str(Path.home())
    filename_profiles = home + "/.dataspine/userdata"
    config = configparser.ConfigParser()
    config.read(filename_profiles)
    account_uuid = config.get('default', 'account-uuid')

    return account_uuid


@authenticate.command()
@click.option('--username', prompt='Username', help='User Name.')
@click.option('--password', prompt='Password', help='User Password.', hide_input=True)
@click.option('--account-uuid', prompt='Account UUID', help='User Account UUID.', hide_input=True)
def login(username, password, account_uuid):
    """Simple program that authenticate user"""

    url = "http://localhost:5000/login"
    encoded_str = encode(username, password)
    header = {
      'x-account-uuid': account_uuid,
      'authorization': encoded_str
    }

    home = str(Path.home())
    filename_userdata = home + "/.dataspine/userdata"
    filename_config = home + "/.dataspine/public-key"

    response = requests.get(url, headers=header)
    public_key = json.loads(response.text)

    config = configparser.ConfigParser()
    config['default'] = {'username': username, 'account-uuid': account_uuid}

    if (response.status_code == 200):

        os.makedirs(os.path.dirname(filename_config), exist_ok=True)
        with open(filename_config, 'w') as f:
            f.write(public_key["public_key"])

        os.makedirs(os.path.dirname(filename_userdata), exist_ok=True)
        with open(filename_userdata, "w") as configfile:
            config.write(configfile)

        keyring.set_password(service_name=account_uuid, username=username, password=password)
        print('Login Succeeded!')
    else:
        print('Invalid credentials!')


@click.group()
def main():
    pass


# @requires_auth
@main.command()
def help():
    """Help command on main group"""
    url = URL + '/help'
    response = requests.get(url).json()
    for f in response['functions']:
        print(f)
    # if (valid_token() == True):
    #     url = URL + '/help'
    #     response = requests.get(url).json()
    #     for f in response['functions']:
    #         print(f)


# @before_filter
@main.command()
def version():
    """Version command on main group"""
    url = URL + '/version'
    response = requests.get(url).json()
    for i in response:
      print(i, response[i], "\n")


@main.command()
@click.option('--model_name', prompt='Model name', help='Model Name.')
@click.option('--model_tag', prompt='Model tag', help='Model Tag.')
@click.option('--model_type', prompt='Model type', help='Model Type.')
@click.option('--model_path', prompt='Model path', help='Model Path.')
# @click.option('--model_runtime', prompt = 'Model runtime', help = 'Model runtime.', required = False, default = None)
def buildmodel(model_name, model_tag, model_type, model_path):
    """Build model command on main group"""

    url = URL + '/buildmodel'
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

    print(response)

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


@main.command()
@click.option('--model_name', prompt='Model name', help='Model Name.')
@click.option('--model_tag', prompt='Model tag', help='Model Tag.')
def modelpush(model_name, model_tag):
    url = URL + '/modelpush'
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


@main.command()
@click.option('--model_name', prompt='Model name', help='Model Name.')
@click.option('--model_tag', prompt='Model tag', help='Model Tag.')
def modelpull(model_name, model_tag):
    url = URL + '/modelpull'
    request = {
        'model_name': model_name,
        'model_tag': model_tag,
    }

    response = requests.post(url, request).json()
    pull_coordinates = response['pull_coordinates']
    cmd = 'docker pull %s' % (pull_coordinates)
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)


@main.command()
@click.option('--model_name', prompt='Model name', help='Model Name.')
@click.option('--model_tag', prompt='Model tag', help='Model Tag.')
def deploy_serverstart(model_name, model_tag):
    url = URL + '/deploy_serverstart'
    request = {
        'model_name': model_name,
        'model_tag': model_tag,
    }

    response = requests.post(url, request).json()
    serverstart_coordinates = response['serverstart_coordinates']
    cmd = 'docker run %s' % (serverstart_coordinates)
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)
    print("")
    print("container name: '%s'" % response['container_name'])
    print("predict port: '%s'" % response['predict_port'])
    print("prometheus port: '%s'" % response['prometheus_port'])
    print("grafana port: '%s'" % response['grafana_port'])
    print("")


@main.command()
@click.option('--model_name', prompt='Model name', help='Model Name.')
@click.option('--model_tag', prompt='Model tag', help='Model Tag.')
@click.option('--model_path', prompt='Model path', help='Model Path.')
def deploy_clusterstart(model_name, model_tag, model_path):
    url = URL + '/deploy_clusterstart'
    request = {
        'model_name': model_name,
        'model_tag': model_tag,
        'model_path': model_tag,
    }

    response = requests.post(url, request).json()

    namespace = response['namespace']
    rendered_yamls = response['rendered_yamls']
    for rendered_yaml in rendered_yamls:
        # For now, only handle '-deploy' and '-svc' and '-ingress' (not autoscale or routerules)
        basePath = os.path.join(os.path.expanduser(model_path))
        filePath = os.path.join(basePath, rendered_yaml)
        f = open(filePath, 'w')
        f.write(yaml.dump(rendered_yaml))
        f.close()
        if ('-stream-deploy' not in rendered_yaml and '-stream-svc' not in rendered_yaml) and (
                    '-deploy' in rendered_yaml or '-svc' in rendered_yaml or '-ingress' in rendered_yaml):
            _istio_apply(yaml_path=rendered_yaml,
                         namespace=namespace)

    model_name = response['model_name']
    image_registry_namespace = response['image_registry_namespace']
    endpoint_url = _get_model_kube_endpoint(model_name=model_name,
                                            namespace=namespace,
                                            image_registry_namespace=image_registry_namespace)

    endpoint_url = endpoint_url.rstrip('/')
    print("Endpoint URL: '%s'" % endpoint_url)


def _istio_apply(yaml_path,
                 namespace=None):
    if not namespace:
        namespace = _default_namespace

    cmd = 'istioctl kube-inject -f %s' % yaml_path
    print("")
    print("Running '%s'." % cmd)
    print("")
    new_yaml_bytes = _subprocess.check_output(cmd, shell=True)
    new_yaml_path = '%s-istio' % yaml_path
    with open(new_yaml_path, 'wt') as fh:
        fh.write(new_yaml_bytes.decode('utf-8'))
        print("'%s' => '%s'" % (yaml_path, new_yaml_path))
    print("")

    cmd = "kubectl apply --namespace %s -f %s" % (namespace, new_yaml_path)
    print("")
    print("Running '%s'." % cmd)
    print("")
    _subprocess.call(cmd, shell=True)
    print("")


def _get_model_kube_endpoint(model_name,
                             namespace,
                             image_registry_namespace):
    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    ingress_name = '%s-%s' % (image_registry_namespace, model_name)
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        ingress = kubeclient_v1_beta1.read_namespaced_ingress(name=ingress_name,
                                                              namespace=namespace)

        endpoint = None
        if ingress.status.load_balancer.ingress and len(ingress.status.load_balancer.ingress) > 0:
            if (ingress.status.load_balancer.ingress[0].hostname):
                endpoint = ingress.status.load_balancer.ingress[0].hostname
            if (ingress.status.load_balancer.ingress[0].ip):
                endpoint = ingress.status.load_balancer.ingress[0].ip

        if not endpoint:
            try:
                istio_ingress_nodeport = _get_istio_ingress_nodeport()
            except Exception:
                istio_ingress_nodeport = '<ingress-controller-nodeport>'

            try:
                istio_ingress_ip = _get_istio_ingress_ip()
            except Exception:
                istio_ingress_ip = '<ingress-controller-ip>'

            endpoint = '%s:%s' % (istio_ingress_ip, istio_ingress_nodeport)

        path = ingress.spec.rules[0].http.paths[0].path

        endpoint = 'http://%s%s' % (endpoint, path)
        endpoint = endpoint.replace(".*", "invocations")

        return endpoint


def _get_istio_ingress_nodeport():
    cmd = "kubectl get svc -n istio-system istio-ingress -o jsonpath='{.spec.ports[0].nodePort}'"
    istio_ingress_nodeport_bytes = _subprocess.check_output(cmd, shell=True)
    return istio_ingress_nodeport_bytes.decode('utf-8')


def _get_istio_ingress_ip():
    cmd = "kubectl -n istio-system get po -l istio=ingress -o jsonpath='{.items[0].status.hostIP}'"
    istio_ingress_nodeport_bytes = _subprocess.check_output(cmd, shell=True)
    return istio_ingress_nodeport_bytes.decode('utf-8')


cli_commands = click.CommandCollection(sources=[authenticate, main])

if __name__ == '__main__':
    cli_commands()