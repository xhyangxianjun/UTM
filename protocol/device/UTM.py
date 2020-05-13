import struct


class USB_Temp_Monitor:
    Device = "UTM"
    Name = "USB温度监控仪"
    Description = ""
    xAxis = [{
        "Name": "CH1",
        "Scale": 1,
    }, {
        "Name": "CH2",
        "Scale": 1,
    }, {
        "Name": "CH3",
        "Scale": 1,
    }, {
        "Name": "CH4",
        "Scale": 1,
    }]

    @staticmethod
    def parsePkg(body):

        # print("Fuuuuck {0}", body)

        (cmd, seq) = struct.unpack(r">BH", body[:3])

        # print("cmd {0:02X} seq {1:04X} ".format(cmd, seq))

        if cmd in b'\x01':

            (h1f, h1, h2f, h2, h3f, h3, h4f, h4) = struct.unpack(
                r">BHBHBHBH", body[3:])

            # print("Fuuuuck")

            return [
                h1/100,
                h2/100,
                h3/100,
                h4/100,
            ]



if __name__ == '__main__':
    a = b'\x01\x01\x01\x00\x08\xfc\x10\x00\x00\x10\x00\x00\x10\x00\x00'

    print("{0}".format(USB_Temp_Monitor.parsePkg(a)))
