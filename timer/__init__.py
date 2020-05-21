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
            time.sleep(self.delay*self.acc*0.1)
            if (old_Die) and (not self.die):
                if not self.onRun is None:
                    self.onRun()

            if not self.die:
                n = datetime.datetime.now()
                dur = n-self.s_Time

                if n > self.next_Time:
                    if not self.fn is None:
                        self.fn()
                    self.next_Time = self.next_Time + \
                        datetime.timedelta(seconds=self.delay) +\
                        datetime.timedelta(milliseconds=self.delay*self.acc)
                    # time.sleep(self.delay*0.9*self.acc)

            if (not old_Die) and (self.die):
                if not self.onStop is None:
                    self.onStop()

            old_Die = self.die

    def Run(self):
        self.die = False
        self.s_Time = datetime.datetime.now()

        self.next_Time = self.s_Time + datetime.timedelta(seconds=self.delay)

    def Stop(self):
        self.die = True

    def runn(self):
        n = datetime.datetime.now()
        dur = n-self.s_Time

        if n > self.next_Time:
            if not self.fn is None:
                self.fn()
            self.next_Time = self.next_Time + \
                datetime.timedelta(seconds=self.delay) +\
                datetime.timedelta(milliseconds=self.delay*self.acc)

        # if dur.total_seconds() > (self.nnn * self.delay):

            #     dur.total_seconds(), self.nnn*self.delay))
            # if int(dur.total_seconds()*(1/self.acc)) != int(self.nnn*self.delay*(1/self.acc)):
            #     dur.total_seconds(),
            #     self.nnn*self.delay,
            # ))
            # self.Stop()
            # exit()

            # print("AAA: {0} {1}".format(dur.total_seconds(), self.nnn))
            # self.a_Time = n
            # self.nnn += 1
            # if self.nnn > 10:
            #     self.nnn = 0
            #     self.s_Time = datetime.datetime.now()

            # time.sleep(self.delay*0)


def round(a):
    if a % 1 > 0.4:
        return int(a)+1
    else:
        return int(a)


if __name__ == '__main__':

    tt = None

    s_Time = datetime.datetime.now()
    nn = 500
    delay = 500

    def fffn():
        global nn
        n = datetime.datetime.now()
        dur = n-s_Time
        # dur = datetime.timedelta(seconds=int(dur.total_seconds()*1000)/1000)
        # print("BBB: {0:.3f}".format(dur.total_seconds()))

        if int(dur.total_seconds()*10)*100 != nn:
            pass
            # tt.Stop()
            # exit()
        nn += delay

        time.sleep(0.45)

    tt = Timer(delay=delay/1000, acc=0.01, fn=fffn)
    tt.Run()
    while(1):
        pass
