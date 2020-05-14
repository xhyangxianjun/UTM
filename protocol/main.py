import io
import serial
import struct
import pkgutil
import sys


header = b"\xF5\xFA"
header_pad = 3

"""
基本协议
Header u16 固定 0xF5,FA
Length u8 下面的字节数
。。。。
CheckSum u8 校验字
"""


def hexString(a):
    s = ""
    for i in a:
        s += "{0:02X} ".format(i)
    return s


def checkSum(data):
    a = 0
    for i in data:
        a += i
    return a % 0x100


def readPackage(r):
    header_count = 0
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
        print("fuuuuuuuck")
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


class BaseProtocol:
    def __init__(self, serial):
        self.s = serial

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


if __name__ == '__main__':
    b = b""
    b += b"\xF5\xFA\x07\x00\x01\x03\xFA"
    b += b"\x00"*1
    b += b"\xF5\xFA\x06\x01\x03\xF9"

    b += b"\xF5\xFA\x0C\x00\x00\x00\x00\x00\x00\x00\x00\xFB"

    # b += b"\xF5\xFA\x0C\x07\x1B\x07\xD0\x0C\x44\xD5"
    # b += b"\x00"*10

    # b += b"\xF5\xFA\x0C\x07\x1B\x07\xD4\x0C\x44\xD9"
    # b += b"\xF5\xFA\x0C\x07\x1B\x07\xD4\x0C\x44\xD9"
    # print("Raw {}".format(hexString(b)))
    # print("CheckSum {0:02X}".format(checkSum(b)))

    sss = serial.Serial(port="com9", baudrate=9600)
    # print(sss.name)
    # print(sss.port)
    # sss.open()

    # br = io.BytesIO(b)

    while(1):
        msg, body = readPackage(sss)
        if msg != None:
            if msg == "EOF":
                break
            # print("Msg: {0}".format(msg))
            continue
        # print("="*10)
        # print("packBody: {0}".format((body)))

        s = ""
        s += "{:02X}-{}".format(body[0],
                                struct.unpack(r">H", body[1:3])[0]/100,)
        s += " "
        s += "{:02X}-{}".format(body[3],
                                struct.unpack(r">H", body[4:6])[0]/100,)
        s += " "
        s += "{:02X}-{}".format(body[6],
                                struct.unpack(r">H", body[7:9])[0]/100,)
        s += " "
        s += "{:02X}-{}".format(body[9],
                                struct.unpack(r">H", body[10:12])[0]/100,)
        print(s)
