import time
import datetime

s = datetime.datetime.now()

a = s

delay = 1
n = 1

while(1):

    ee = datetime.datetime.now() - s

    if ee.total_seconds() > (delay*n):
        n+=1

        dur = datetime.datetime.now() - a
        print("{0} {1}".format(
            ee,
            ee.total_seconds(),
        ))
        time.sleep(delay*0.95)

    time.sleep(delay*0.01)
