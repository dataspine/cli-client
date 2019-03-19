#-*- coding: utf-8 -*-
import json
import click
import os
import requests
from utils import get_header_basic_auth
from utils import API_URL_BASE, PUBLIC_KEY_PATH, KUBE_CONFIG_PATH, API_SERVER
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import kubernetes.client as _kubeclient
import kubernetes.config as _kubeconfig
import warnings as _warnings
import base64
import yaml
import subprocess as _subprocess
from tabulate import tabulate


@click.group()
def cluster():
    """The family commands to work with cluster"""
    pass


@cluster.command('list')
def list_clusters():
    url = '{}/clusters/list'.format(API_URL_BASE)
    headers = get_header_basic_auth()
    clusters = requests.get(url, headers=headers)
    clusters = json.loads(clusters.text)

    clusters_list = []
    for cluster in clusters["items"]:
        clusters_list.append([cluster['cluster_name'], cluster['cluster_alias']])
    print(tabulate(clusters_list, headers=["Name", "Alias"], tablefmt='orgtbl'))


@cluster.command('init')
@click.option('--cluster', 'cluster_name', prompt='Cluster name', help='The name of the cluster')
@click.option('--namespace', 'cluster_namespace', help='The name of the cluster')
def cluster_init(cluster_name, cluster_namespace=None):
    url = '{}/clusters/init'.format(API_URL_BASE)
    headers = get_header_basic_auth()

    body = {
        "cluster_name": cluster_name,
    }

    if cluster_namespace:
        body['cluster_namespace'] = cluster_namespace

    response = requests.put(url, headers=headers, json=body)
    # import pdb; pdb.set_trace()
    if response.status_code == 200:
        response_json = json.loads(response.text)
        print(response_json.get('message'))
    else:
        print('Unable to initialize cluster')



@cluster.command()
@click.option('--config', prompt='Kubeconfig path', help='The path to the configuration file for kubernetes', type=click.Path(exists=True))
@click.option('--name', 'name', prompt='Cluster name', help='The name of the cluster')
@click.option('--alias', 'alias', prompt="Cluster alias", help='The alias of the cluster')
@click.option('--description', help='The description or purpose of the cluster')
def add(config, name, alias, description=""):
    """Creates a cluster for the account"""

    url = '{}/clusters/create'.format(API_URL_BASE)
    headers = get_header_basic_auth()

    body_cluster = {
        "cluster_name": name,
        "cluster_alias": alias,
        "cluster_description": description
    }

    response = requests.post(url, headers=headers, json=body_cluster)
    response_json = json.loads(response.text)
    if response.status_code != 201:
        print(response_json['message'])
        return

    check_for_pk()
    with open(PUBLIC_KEY_PATH, 'r') as public_key_file:
        public_key = public_key_file.read()
    with open(config, 'r') as kube_config:
        kube_config_file = kube_config.read()
    encrypted_config_file = encrypt_message(kube_config_file, public_key)
    # print (response_json["id_cluster"])
    # print(encrypted_config_file.decode("utf-8"))id_cluster
    upload_config_request_data = {
        "id_cluster": response_json["id_cluster"],
        "config": encrypted_config_file.decode("utf-8")
    }

    url = '{}/clusters/upload_config'.format(API_URL_BASE)
    updated = requests.put(url, headers=headers, json=upload_config_request_data)
    updated_json = json.loads(updated.text)
    if updated.status_code != 200:
        print(updated_json['message'])
        return

    print("Cluster created and config updated")


@click.option('--model_name', prompt='Model name', help='Model Name.')
@click.option('--model_tag', prompt='Model tag', help='Model Tag.')
def deploy_serverstart(model_name, model_tag):
    url = API_URL_BASE + '/deploy_serverstart'
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


def check_for_pk():
    if not os.path.isfile(PUBLIC_KEY_PATH):
        print('Please login! Run \'dataspine login\'')


def encrypt_message(blob, public_key):
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted = ""
    encrypted = bytes(encrypted.encode('utf-8'))

    while not end_loop:
        chunk = blob[offset:offset + chunk_size]

        if len(chunk) % chunk_size != 0:
            end_loop = True
            chunk += " " * (chunk_size - len(chunk))

        new_chunk = rsa_key.encrypt(bytes(chunk.encode('utf-8')))
        encrypted += new_chunk
        offset += chunk_size
    return base64.b64encode(encrypted)


def decrypt_blob(encrypted_blob, private_key):

    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    encrypted_blob = base64.b64decode(encrypted_blob)

    chunk_size = 512
    offset = 0
    decrypted = ""
    decrypted = bytes(decrypted.encode('utf-8'))

    while offset < len(encrypted_blob):
        chunk = encrypted_blob[offset: offset + chunk_size]
        new_chunk = rsakey.decrypt(chunk)
        decrypted += new_chunk
        offset += chunk_size

    return decrypted


def decrypt_message(encoded_encrypted_msg, privatekey):
    privatekey = RSA.importKey(privatekey)
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
    return decoded_decrypted_msg


def _istio_apply(yaml_path,
                 namespace=None):
    # if not namespace:
        # namespace = _default_namespace

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


def _get_istio_ingress_nodeport():
    cmd = "kubectl get svc -n istio-system istio-ingress -o jsonpath='{.spec.ports[0].nodePort}'"
    istio_ingress_nodeport_bytes = _subprocess.check_output(cmd, shell=True)
    return istio_ingress_nodeport_bytes.decode('utf-8')


def _get_istio_ingress_ip():
    cmd = "kubectl -n istio-system get po -l istio=ingress -o jsonpath='{.items[0].status.hostIP}'"
    istio_ingress_nodeport_bytes = _subprocess.check_output(cmd, shell=True)
    return istio_ingress_nodeport_bytes.decode('utf-8')


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

