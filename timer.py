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
        self.nnn = 0

        self.fn = fn

        self.setDaemon(True)
        self.start()

    def run(self):
        old_Die = self.die
        while(1):
            if (old_Die) and (not self.die):
                if not self.onRun is None:
                    self.onRun()

            if not self.die:
                self.runn()

            if (not old_Die) and (self.die):
                if not self.onStop is None:
                    self.onStop()

            old_Die = self.die
            time.sleep(self.delay*self.acc*0.1)

    def Run(self):
        self.die = False
        self.s_Time = datetime.datetime.now()

    def Stop(self):
        self.die = True

    def runn(self):
        n = datetime.datetime.now()
        dur = n-self.s_Time

        if dur.total_seconds() > (self.nnn * self.delay):

            # print("Fuuuuck 000 {0} {1}".format(
            #     dur.total_seconds(), self.nnn*self.delay))
            if int(dur.total_seconds()*(1/self.acc)) != int(self.nnn*self.delay*(1/self.acc)):
                print("Fuuuuck 111 {0} {1}".format(
                    dur.total_seconds(),
                    self.nnn*self.delay,
                ))
                self.Stop()
                exit()

            if not self.fn is None:
                self.fn()

            # print("AAA: {0} {1}".format(dur.total_seconds(), self.nnn))
            self.a_Time = n
            self.nnn += 1
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
    nn = 0
    delay = 0.5

    def fffn():
        global nn
        n = datetime.datetime.now()
        dur = n-s_Time
        dur = datetime.timedelta(seconds=round(dur.total_seconds()*100)/100)
        # print("BBB: {0}".format(dur.total_seconds()))

        if round(dur.total_seconds()*20) != round(nn*20):
            print("Fuuuuck 222 {0} {1}".format(dur.total_seconds(), nn))
            tt.Stop()
            # exit()
        nn += (delay)

        # time.sleep(0.1)

    tt = Timer(delay=delay, acc=0.05, fn=fffn)
    tt.Run()
    while(1):
        pass
