import os

def gen_config_from_file(fname):
    config_dict = {}
    try:
        with open(fname, "r") as config:
            for item in config:
                item = item.split("=")
                if "url" in item[0]:
                    if "http" not in item[1]:
                        item[1] = "http://" + item[1]
                config_dict[item[0].strip()] = item[1].strip()
    except FileNotFoundError:
        raise FileNotFoundError("Please properly configure the module by creating aotsapi.config! (You may use aotsapi.config.example as an example)")
    return config_dict


global config_params

path = os.path.dirname(__file__)

config_params = gen_config_from_file(os.path.join(path, "aotsapi.config"))

from .processing import *
from .api_calls import *
