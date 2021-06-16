import traceback
try:
    num = int('abc')
except Exception:
    traceback.print_exc()

traceback.print_exc()  # 直接打印异常
traceback.format_exc()  # 返回字符串
traceback.print_exc(file=open("error.txt", "a+"))
