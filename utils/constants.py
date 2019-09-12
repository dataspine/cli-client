# -*- coding: utf8 -*-
from pathlib import Path

HOME = str(Path.home())

BASE_URL = 'http://localhost'
BASE_URL_BACKEND = 'http://localhost:5001/api/v1'
BASE_API_SERVER = 'http://localhost'
PORT = 5000
API_URL_BASE = "{}:{}".format(BASE_API_SERVER, PORT)
API_BACKEND = "{}:{}".format(BASE_URL_BACKEND, PORT)
API_SERVER = "{}:{}".format(BASE_API_SERVER, PORT)

USERDATA_PATH = HOME + "/.dataspine/userdata"
PUBLIC_KEY_PATH = HOME + "/.dataspine/public-key"
KUBE_CONFIG_PATH = HOME + '/.kube/config'

