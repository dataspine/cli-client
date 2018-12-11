# -*- coding: utf8 -*-
from pathlib import Path

HOME = str(Path.home())

BASE_URL = 'http://localhost'
BASE_URL_BACKEND = 'http://35.243.188.142'
PORT = 5000
API_URL_BASE = "{}:{}".format(BASE_URL, PORT)
API_BACKEND = "{}:{}".format(BASE_URL_BACKEND, PORT)

USERDATA_PATH = HOME + "/.dataspine/userdata"
PUBLIC_KEY_PATH = HOME + "/.dataspine/public-key"
KUBE_CONFIG_PATH = HOME + '/.kube/config'

