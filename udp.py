import threading
import time
from socket import *
import numpy as np
import matplotlib.pyplot as plt

prev_sensor = np.zeros(8)
colors = ['b', 'r', 'y', 'g', 'c', 'k', 'm', '#e41a1c']
plot_num = 10   # plotされるセンサ値の数
plot_idx = 0

def plot_sensor_data_bar(sensor_data, interval=0.01):
    x = np.arange(0, len(sensor_data), 1)
    # 前の描画が残っているので白で上書き
    global prev_sensor
    plt.bar(x, prev_sensor, color='white')
    plt.bar(x, sensor_data, color='blue')
    prev_sensor = sensor_data
    plt.pause(interval)


def plot_sensor_data(sensor_data, interval=0.01):
    global plot_idx, plot_num, prev_sensor
    plot_range = [plot_idx - 1, plot_idx]

    for p_data, data, color in zip(prev_sensor, sensor_data, colors):
        plt.plot(plot_range, [p_data, data], color=color)
    plot_idx += 1
    plt.draw()
    plt.xlim(plot_idx - plot_num, plot_idx)
    # plt.ylim(0, 3)
    prev_sensor = sensor_data
    plt.pause(interval)
    if plot_idx % (plot_num*4) == 0:
        plt.close()
        plt.figure()


class ReceiveThread(threading.Thread):
    def __init__(self, PORT=12345):
        threading.Thread.__init__(self)
        self.data = 'hoge'
        self.kill_flag = False
        # line information
        self.HOST = "127.0.0.1"
        self.PORT = PORT
        self.BUFSIZE = 1024
        self.ADDR = (gethostbyname(self.HOST), self.PORT)
        # bind
        self.udpServSock = socket(AF_INET, SOCK_DGRAM)
        self.udpServSock.bind(self.ADDR)
        self.received = False

    def get_data(self):
        data_ary = []
        for i in range(8):
            num = int(str(self.data[i*8:(i+1)*8]))
            data_ary.append(num / 167.0 / 10000)
        self.received = False
        return data_ary

    def run(self):
        while True:
            try:
                data, self.addr = self.udpServSock.recvfrom(self.BUFSIZE)
                self.data = data.decode()
                self.received = True
            except:
                pass


if __name__ == '__main__':
    th = ReceiveThread()
    th.setDaemon(True)
    th.start()
    plt.ion()

    while True:
        if not th.data:
            break

        if th.received:
            sensor_data = th.get_data()
            d = np.sqrt((19.1286**(3/2))/sensor_data[4])
            print(d)

            # 両方は使用不可
            # plot_sensor_data(sensor_data)
            # plot_sensor_data_bar(sensor_data)

        time.sleep(1)
