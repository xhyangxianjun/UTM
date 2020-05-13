
class VB_Mind_H2:
    Device = "VB_Mind_H2"
    Name = "H2_VB_Mind-调试通讯协议"
    Description = "VB_Mind_H2"
    xAxis = [
        {"Name": "温度,入水口"},
        {"Name": "温度,出水口"},
        {"Name": "Bump_PWM_Duty"},
        {"Name": "Water_Temp_Set"},
        {"Name": "KeKongGui_DaoTon_Count"},
        {"Name": "All_Bit"},
        {"Name": "PID_P"},
        {"Name": "PID_I"},
        {"Name": "K"}
    ]

    @staticmethod
    def parsePkg(body):
        return


