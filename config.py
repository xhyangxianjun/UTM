# import configparser

import yaml
import io

# cfg = configparser.ConfigParser()

default_config = {
    "serial":{
        "baud": 9600,
        "deviceType": "UTM",
        "port": "COM1",
    },
}


class CFG:
    data = None
    cfgPath = "config.yml"
    encoding = "utf8"

def loadConfig():
    with open(CFG.cfgPath, 'r', encoding=CFG.encoding) as stream:
        try:
            CFG.data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def saveConfig():
    with io.open(CFG.cfgPath, 'w', encoding=CFG.encoding) as outfile:
        yaml.dump(CFG.data, outfile, default_flow_style=False,
                  allow_unicode=True)
