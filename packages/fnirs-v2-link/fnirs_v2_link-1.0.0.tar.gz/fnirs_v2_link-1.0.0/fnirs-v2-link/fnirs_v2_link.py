# -*- coding:utf8 -*-

import threading
import time
import json
from websocket import create_connection

from connection import Connection
from sys_version import SysVersion


# 数据处理
class DataProcessing(threading.Thread):
    _ws = None
    running = False

    def __init__(self):
        super(DataProcessing, self).__init__()
        self.running = True
        try:
            self._ws = create_connection(Connection().WS_GETDATA_URL)
        except Exception as e:
            self._ws = None
            print('服务端未开启!')

    def run(self):
        if self._ws is None:
            return
        print('开始数据处理!')
        while self.running:
            result = self._ws.recv()  ##接收消息
            if result is not None:
                # result = result.encode('utf-8')
                print(result)

if __name__ == '__main__':
    # 启动数据处理线程
    thread = DataProcessing()
    thread.start()

    con = Connection()
    start = time.time()

    # 触发开始
    data = con.start()
    # 打印连接返回信息
    print(data)

    # 判断是否连接成功
    if data['success'] is True:
        end = time.time()
        # 打印平均响应时间
        # print(end - start)

        # 读取1min的数据
        time.sleep(1 * 60)

        # 任意时间段打标
        con.mark(2)

        # 读取1min的数据
        time.sleep(1 * 60)

        # 结束测试
        data = con.stop()
        print(data)

        # 结束数据处理线程
        thread.running = False
