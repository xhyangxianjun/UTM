import threading
import time
import datetime


class Timer (threading.Thread):
    def __init__(self, delay=1, acc=0.1, fn=None):
        threading.Thread.__init__(self)
        self.die = True
        self.delay = delay
        self.acc = acc

        self.onStop = None
        self.onRun = None

        self.s_Time = None
        self.a_Time = None

        self.next_Time = None
        self.nnn = 0

        self.fn = fn

        self.setDaemon(True)
        self.start()

    def run(self):
        old_Die = self.die
        while(1):
            if (old_Die) and (not self.die):
                if self.onRun is not None:
                    self.onRun()

            if not self.die:
                n = datetime.datetime.now()

                if n > self.next_Time:
                    if self.fn is not None:
                        self.fn()
                    self.next_Time = self.next_Time + \
                        datetime.timedelta(seconds=self.delay) +\
                        datetime.timedelta(milliseconds=self.delay*self.acc)
                    # time.sleep(self.delay*0.9*self.acc)

            if (not old_Die) and (self.die):
                if self.onStop is not None:
                    self.onStop()

            old_Die = self.die
            time.sleep(self.delay*self.acc*0.1)

    def Run(self):
        self.die = False
        self.s_Time = datetime.datetime.now()

        # self.next_Time = self.s_Time + datetime.timedelta(seconds=self.delay)
        self.next_Time = self.s_Time

    def Stop(self):
        self.die = True

    def runn(self):
        n = datetime.datetime.now()

        if n > self.next_Time:
            if self.fn is not None:
                self.fn()
            self.next_Time = self.next_Time + \
                datetime.timedelta(seconds=self.delay) +\
                datetime.timedelta(milliseconds=self.delay*self.acc)


def round(a):
    if a % 1 > 0.4:
        return int(a)+1
    else:
        return int(a)


if __name__ == '__main__':

    tt = None
    cnt = 0
    s_Time = datetime.datetime.now()

    def fffn():
        global cnt
        dur = datetime.datetime.now() - s_Time

        dur = datetime.timedelta(
            milliseconds=round(dur.total_seconds()*100)*10)

        print("{0} {1}".format(cnt, dur))

        cnt += 1

    tt = Timer(delay=1, acc=0.1, fn=fffn)
    tt.Run()
    while(1):
        pass
