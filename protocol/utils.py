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

def HexDump(a):
    s = "     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\r\n"
    for k, v in enumerate(a):
        if k % 0x10 == 0x0:
            s += "{0:02X}: ".format(k)

        s += "{0:02X} ".format(v)

        if k % 0x10 == 0xF:
            s += "\r\n"
    return s