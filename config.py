# import configparser

import yaml
import json
import io
import protocol
import os

cwd = os.getcwd()

# print("cmd: {0}".format(cwd))

# cfg = configparser.ConfigParser()

baudList = [
    "50", "75", "110", "134", "150", "200", "300", "600",
    "1200", "1800", "2400", "4800", "9600",
    "19200", "38400", "57600", "115200"]
# baudList = [
#     "50", "75", "110", "134", "150", "200", "300", "600",
#     "1200", "1800", "2400", "4800", "9600",
#     "19200", "38400", "57600", "115200"]

default_config_device = {
    "name": "device1",
    "baud": "9600",
    "deviceType": "UTM",
    "port": "COM1",
    "chann": [0, 1, 2, 3],
}

default_config = {
    "serial": [],
    "webchart": {
        "animation": True,
        "symbol": True,
    },
}


class CFG_Chart:
    """
    配置信息：图表
    """

    def __init__(self,
                 cfg_dict=None,
                 isLinkEmpty=False,
                 enAnimation=False,
                 chartRefreshInterval=0.1,
                 ):
        if cfg_dict is None:
            self.isLinkEmpty = isLinkEmpty
            self.enAnimation = enAnimation
            self.chartRefreshInterval = chartRefreshInterval
        else:
            self.isLinkEmpty = cfg_dict.get("isLinkEmpty", isLinkEmpty)
            self.enAnimation = cfg_dict.get("enAnimation", enAnimation)
            self.chartRefreshInterval = cfg_dict.get(
                "chartRefreshInterval", chartRefreshInterval)

    def to_dict(self):
        return {
            "isLinkEmpty": self.isLinkEmpty,
            "enAnimation": self.enAnimation,
            "chartRefreshInterval": self.chartRefreshInterval,
        }


class CFG_View:
    """
    配置信息：显示
    """

    def __init__(self,
                 cfg_dict=None,
                 showLiveData=False,
                 showLatestView=0,
                 ):

        if cfg_dict is None:
            self.showLiveData = showLiveData
        else:
            self.showLiveData = cfg_dict.get("showLiveData", showLiveData)
        self.showLatestView = cfg_dict.get("showLatestView", showLatestView)

    def to_dict(self):
        return {
            "showLiveData": True if self.showLiveData else False,
            "showLatestView": self.showLatestView,
        }


class Serial:
    """
    配置信息：通讯参数
    """

    def __init__(self,
                 cfg_dict=None,
                 port="COM1", baud="9600",
                 deviceType="UTM", name="Device1", sel_chann=[]):

        if cfg_dict is None:
            self.port = port
            self.baud = baud
            self.deviceType = deviceType
            self.name = name
            self.sel_chann = sel_chann
        else:
            self.port = cfg_dict.get("port", port)
            self.baud = cfg_dict.get("baud", baud)
            self.deviceType = cfg_dict.get("deviceType", deviceType)
            self.name = cfg_dict.get("name", name)
            self.sel_chann = cfg_dict.get("chann", sel_chann)

    def to_dict(self):
        return {
            "port": self.port,
            "baud": self.baud,
            "deviceType": self.deviceType,
            "name": self.name,
            "sel_chann": self.sel_chann,
        }


class CFG:
    data = None
    gCfg = None
    cfgPath = os.path.join(cwd, "config.yml")

    encoding = "utf8"

    def __init__(self, cfg_dict):
        self.serial_list = []
        for i in cfg_dict["serial"]:
            self.serial_list.append(Serial(cfg_dict=i))
        self.chart = CFG_Chart(cfg_dict.get("chart"))
        self.view = CFG_View(cfg_dict.get("view"))

        self.orl_json = json.dumps(cfg_dict, sort_keys=True)

    # @staticmethod
    # def currentProtocol():
    #     for i in protocol.M:
    #         if i.Device == CFG.data["serial"]["deviceType"]:
    #             return i

    # @staticmethod
    # def currentProtocol(tt):
    #     for i in protocol.M:
    #         if i.Device == tt:
    #             return i

    # @staticmethod
    # def filterList(d):
    #     dd = []
    #     for k, v in enumerate(d):
    #         if k in CFG.data["serial"]["chann"]:
    #             dd.append(v)
    #     return dd

    # @staticmethod
    # def filterAxis():
    #     ret = []
    #     for k, v in enumerate(self.data["serial"]):
    #     return CFG.filterList(CFG.currentProtocol().xAxis)

    @staticmethod
    def getProtocol_By_DeiceName(name):
        for k1, v1 in enumerate(protocol.M):
            if v1.Device == name:
                return v1

    @staticmethod
    def getAllCurChannel_Comp():
        channs = []
        for k, v in enumerate(CFG.data["serial"]):
            prot = None
            for k1, v1 in enumerate(protocol.M):
                if v1.Device == v["deviceType"]:
                    prot = v1
                    break
            for k1, v1 in enumerate(prot.xAxis):
                if k1 in v["chann"]:
                    vv = v1.copy()
                    vv["Name"] = "{0}-{1}".format(v["name"], v1["Name"])
                    channs.append(vv)
        return channs

    @staticmethod
    def getAllCurChannel():
        channs = []
        for k, v in enumerate(CFG.data["serial"]):
            xAxis = []
            prot = None
            for k1, v1 in enumerate(protocol.M):
                if v1.Device == v["deviceType"]:
                    prot = v1
                    break

            for k1, v1 in enumerate(prot.xAxis):
                if k1 in v["chann"]:
                    vv = v1.copy()
                    xAxis.append(vv)
            channs.append({
                "Device": prot.Device,
                "DName": prot.Name,
                "Protcol": prot,
                "xAxis": xAxis,
                "Name": v["name"]
            })
        return channs


def loadConfig():
    with open(CFG.cfgPath, 'r', encoding=CFG.encoding) as stream:
        try:
            CFG.data = yaml.safe_load(stream)
            CFG.gCfg = CFG(CFG.data)

        except yaml.YAMLError as exc:
            print(exc)


def saveConfig():
    CFG.data["view"] = CFG.gCfg.view.to_dict()
    CFG.data["chart"] = CFG.gCfg.chart.to_dict()
    new_json = json.dumps(CFG.data, sort_keys=True)
    if new_json == CFG.gCfg.orl_json:
        # print("CFG is no change")
        return
    print("Config file change, save to: {0}".format(CFG.cfgPath))
    with io.open(CFG.cfgPath, 'w', encoding=CFG.encoding) as outfile:
        yaml.dump(CFG.data, outfile, default_flow_style=False,
                  allow_unicode=True)
