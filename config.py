# import configparser

import yaml
import io
import protocol
import os

cwd = os.getcwd()

# print("cmd: {0}".format(cwd))

# cfg = configparser.ConfigParser()

default_config = {
    "serial": {
        "baud": 9600,
        "deviceType": "UTM",
        "port": "COM1",
    },
    "webchart": {
        "animation": True,
        "symbol": True,
    }
}


class CFG:
    data = None
    cfgPath = os.path.join(cwd, "config.yml")

    encoding = "utf8"

    @staticmethod
    def currentProtocol():
        for i in protocol.M:
            if i.Device == CFG.data["serial"]["deviceType"]:
                return i


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
