import struct
import typing

import serial

from .utils import checkSum


class BaseProtocol:

    ProtocolType_Std_1 = 0  # 标准协议
    ProtocolType_T87_RS232 = 1  # 87系列电参RS232通讯协议
    ProtocolType_Fake = 2 # 测试用生成的假数据

    def __init__(self, serialA):
        self.s = serialA
        self.type = BaseProtocol.ProtocolType_Std_1  # 默认
        self.M_Btn: Btn_Func_Dir = None

    def sendPackage(self, body):
        s = b"\xF5\xFA"
        s += struct.pack(">B", len(body)+4)
        s += body
        s += struct.pack(">B", checkSum(s))

        try:
            if self.s.is_open:
                self.s.write(s)
                self.s.flush()
        except serial.serialutil.SerialException as e:
            raise e

    def sendPackageRaw(self, body):
        try:
            if self.s.is_open:
                self.s.write(body)
                self.s.flush()
        except serial.serialutil.SerialException as e:
            raise e

    def onOpen(self):
        pass


header = b"\xF5\xFA"
header_pad = 3

"""
基本协议
Header u16 固定 0xF5,FA
Length u8 当前帧的字节数
。。。。
CheckSum u8 校验字
"""


def recvPkg_ProtocolType_Std_1(r):
    for i in range(len(header)):
        b = r.read(1)
        if len(b) < 1:
            return "EOF", None
        if b[0] != header[i]:
            return "Miss Header", None
    b = r.read(1)
    if len(b) < 1:
        return "EOF", None
    packLen = b[0]
    if packLen < header_pad:
        return "Miss Length", None
    packBody = r.read(packLen-header_pad)
    if len(packBody) < packLen-header_pad:
        print("packBody {0} packLen {1}".format(len(packBody), packLen))
        print("packBody: {0}".format(packBody))
        return "EOF", None

    checkBuf = b""
    checkBuf += header
    checkBuf += bytes([packLen])
    checkBuf += packBody[:-1]
    c = checkSum(checkBuf)

    if c != packBody[-1]:
        # print("packLen: {0:02X}".format(packLen))
        # print("checkBuf: {0}".format(checkBuf))
        # print("packBody: {0}".format(packBody))
        # print("c: {0:x}".format(c))
        return "CheckSum Fail", None

    return None, packBody[:-1]


"""
电参通讯协议
Start u8 固定 0x7D
Addr 3byte 设备地址的ASCII
Data X 数据的ASCII
CheckSum 3byte 校验字的ASCII
Stop u8 固定 0x7F
"""


def recvPkg_ProtocolType_T87_RS232(r):
    b = r.read(1)
    if b != b"\x7D":
        return "Missing Header", None

    packBody = b""

    while True:
        b = r.read(1)
        if b == b"\x7E":
            break
        packBody += b

    if len(packBody) < 6:
        return "Missing Length", None

    # print("packBody {0} packLen {1}".format(packBody, len(packBody)))

    # dev_addr = packBody[0:3]
    # checkSum = packBody[-4:-1]

    return None, packBody


recvFM = {}
recvFM[BaseProtocol.ProtocolType_Std_1] = recvPkg_ProtocolType_Std_1
recvFM[BaseProtocol.ProtocolType_T87_RS232] = recvPkg_ProtocolType_T87_RS232


class Btn_Base():
    def __init__(self, name: str):
        self.name = name


class Btn_Func(Btn_Base):
    def __init__(self, name: str, func):
        super().__init__(name)
        self.func = func


class Btn_Func_Dir(Btn_Base):
    def __init__(self, name: str, btn_items: typing.List[Btn_Base] = []):
        super().__init__(name)
        self.btn_items = btn_items


Input_Type_Num_Uint8: str = "uint8"  # 选择框
Input_Type_Num_Uint16: str = "uint16"  # 选择框
Input_Type_Num_Uint32: str = "uint32"  # 选择框
Input_Type_Select: str = "select"  # 选择框


class Btn_Input_Opt(Btn_Base):

    def __init__(
            self,
            name: str,
            default_value="",
            key: str = None,
            opt_type: str = Input_Type_Num_Uint16):
        super().__init__(name)
        self.opt_type = opt_type
        self.default_value = default_value

    def Valid(self, value):
        value_c = 0

        try:
            if self.opt_type == Input_Type_Num_Uint8:
                value_c = int(value)
                if (value_c >= 0) and (value_c < (1 << 8)):
                    return True, value_c
            elif self.opt_type == Input_Type_Num_Uint16:
                value_c = int(value)
                if (value_c >= 0) and (value_c < (1 << 16)):
                    return True, value_c
            elif self.opt_type == Input_Type_Num_Uint32:
                value_c = int(value)
                if (value_c >= 0) and (value_c < (1 << 32)):
                    return True, value_c
        except ValueError:
            pass
        return False, 0


class Btn_Input(Btn_Base):
    def __init__(self,
                 name: str,
                 func,
                 desc: str = "",
                 opts: Btn_Input_Opt = [],
                 ):
        super().__init__(name)
        self.func = func
        self.opts = opts
        self.description = desc


class XAxis:
    def __init__(self, name, ID=None, scale=1):
        self.name = name
        self.scale = scale

        if ID is None:
            self.ID = name
