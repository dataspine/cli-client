#-*- coding: utf-8 -*-
import os
import json
import ssl
import click
import requests
import subprocess as _subprocess
from urllib.request import urlopen
import os.path
from utils import API_URL_BASE, API_SERVER
from utils import get_header_basic_auth
from tabulate import tabulate


@click.group()
def get():
    """The family commands to work with lists"""
    pass


@get.command('deployments')
@click.option('--cluster name', 'clustername', prompt='Cluster name', help='The name of the cluster')
def getdeployments(clustername):
    url = API_URL_BASE + '/getdeployments'
    headers = get_header_basic_auth()

    body = {
        'cluster_name': clustername
    }
    try:
        response = requests.get(url, headers=headers, json=body).json()
        deployments_list = []
        items =  response["items"]
        for deployment in items:
            deployments_list.append(
            [deployment["metadata"]["name"], deployment["metadata"]["namespace"]])
        print(tabulate(deployments_list, headers=[
        "Deployments", "Namespace"], tablefmt='orgtbl'))

    except KeyError:
        error = 'Something went wrong'
        print(error)

@get.command('services')
@click.option('--cluster name', 'clustername', prompt='Cluster name', help='The name of the cluster')
def getdeployments(clustername):
    url = API_URL_BASE + '/getservices'
    headers = get_header_basic_auth()

    body = {
        'cluster_name': clustername
    }
    try:
        response = requests.get(url, headers=headers, json=body).json()
        deployments_list = []
        items =  response["items"]
        for deployment in items:
            deployments_list.append(
            [deployment["metadata"]["name"], deployment["metadata"]["namespace"]])
        print(tabulate(deployments_list, headers=[
        "Services", "Namespace"], tablefmt='orgtbl'))

    except KeyError:
        error = 'Something went wrong'
        print(error)