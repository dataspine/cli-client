# -*- coding: utf8 -*-
from pathlib import Path

HOME = str(Path.home())

# BASE_URL = 'http://localhost'
BASE_URL_BACKEND = 'http://35.239.205.69'
BASE_API_SERVER = 'http://35.232.205.144'

PORT = 80
# PORT1 = 5000
# PORT2 = 5001

API_URL_BASE = "{}:{}".format(BASE_API_SERVER, PORT)
API_BACKEND = "{}:{}".format(BASE_URL_BACKEND, PORT)
API_SERVER = "{}:{}".format(BASE_API_SERVER, PORT)


USERDATA_PATH = HOME + "/.dataspine/userdata"
PUBLIC_KEY_PATH = HOME + "/.dataspine/public-key"
KUBE_CONFIG_PATH = HOME + '/.kube/config'

