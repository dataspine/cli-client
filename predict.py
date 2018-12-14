#-*- coding: utf-8 -*-
import os
import json
import ssl
import click
import requests
import subprocess as _subprocess
from urllib.request import urlopen
import os.path
from utils import API_URL_BASE
from utils import get_header_basic_auth

@click.group()
def predict():
    """The family commands to work with predict"""
    pass


@predict.command('route')
@click.option('--model name', 'model', prompt='Model name', help='The name of the model')
@click.option('--weights', 'model_split_tag_and_weight_dict', prompt='Weights with model tags', help='Provide weights along with model tags i.e. {"a": 100, "b": 0, "c": 0}')
@click.option('--shadow weights', 'model_shadow_tag_list', prompt='Shadow model tags', help='Provide shadow model tags i.e. [b, c] Note: must set b and c to traffic split 0 above')
def routetraffic(model, model_split_tag_and_weight_dict, model_shadow_tag_list):
    """Route traffic between different versions"""

    url = API_URL_BASE + '/predict-route'
    headers = get_header_basic_auth()
    #print(model_split_tag_and_weight_dict)
    body = {
        'model_split_tag_and_weight_dict': model_split_tag_and_weight_dict,
        'model_shadow_tag_list': model_shadow_tag_list,
        'model_name': model,
    }
    try:
        response = requests.post(url, headers=headers, json=body).json()
        print('Status:' , response['status'])
        print('Routes:',  response['new_traffic_split_routes'])
        print('Shadow tags:', response['new_traffic_shadow_routes'])

    except KeyError:
        error = 'Something went wrong'
        print(error)
    
