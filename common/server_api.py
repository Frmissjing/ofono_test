'''
Author: Frmissjing 892153623@qq.com
Date: 2023-11-22 18:15:08
LastEditors: Frmissjing 892153623@qq.com
LastEditTime: 2024-05-30 18:34:07
FilePath: /ofono_test/common/server_api.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
#!/usr/bin/python3
import socket
# 导入线程模块
import threading
import select
import sys

buff1 = []
buff2 = []
global innoServer

class InnoServer(object):
    'InnoServer'
    Conn = {"Unsolicated":None, "Response":[]}
    CurrespConn = None
    thread = []

    def __init__(self):
        # 创建服务端套接字对象
        self.ServerSk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # 设置端口复用，程序退出后端口马上释放
        self.ServerSk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    
        # 绑定端口
        self.ServerSk.bind(('127.0.0.1',12345))
    
        # 设置监听
        self.ServerSk.listen(3)

    def GetSocket(self):
        return self.ServerSk

    def SetUnsolicatedConn(self,conn):
        self.Conn["Unsolicated"] = conn

    def SetResponseConn(self, conn):
        self.Conn["Response"].append(conn)

    def SetCurrespConn(self, conn):
        self.CurrespConn = conn


# 接收下发通道数据
def handle_client1_request(conn, addr):
    global buff1
    # 循环接收数据
    while True:
        recv_data = conn.recv(4096)
        
        # 如果接收到数据，就村到buff
        if recv_data:
            print("客户端是:", addr)
            print("客户端发来的消息是:", recv_data.decode('utf-8'))
            buff1.apepend(recv_data.decode('utf-8'))


# 接收下发通道数据
def handle_client3_request(conn, addr):
    global buff3
    # 循环接收数据
    while True:
        recv_data = conn.recv(4096)
        
        # 如果接收到数据，就村到buff
        if recv_data:
            print("客户端是:", addr)
            print("客户端发来的消息是:", recv_data.decode('utf-8'))
            buff3.apepend(recv_data.decode('utf-8'))


def InnoServerMain():
    global buff1, buff3
    inputs = []
    outputs = [] 
    # 创建InnoServer
    innoServer = InnoServer()

    sk = innoServer.GetSocket()
    inputs.append(sk)

    # 等待第一个Client连接(通道1，下发通道1)
    ClientConn1, ClientAddr1 = sk.accept()
    print("Channal1 connect from ", ClientAddr1)
    innoServer.SetResponseConn(ClientConn1)
    inputs.append(ClientConn1)
    # # 创建线程对象,将接收到的数据存到buff
    # thd = threading.Thread(target = handle_client1_request, args = (ClientConn1, ClientAddr1))
    # innoServer.thread.append(thd)
    # thd.setDaemon(True)
    # thd.start()

    # 等待第二个Client连接(通道2,主动上报通道)
    ClientConn, ClientAddr = sk.accept()
    print("unsol Channal connect from ", ClientAddr1)
    innoServer.SetResponseConn(ClientConn)


    # 等待第三个Client连接(通道3,下发通道2)
    ClientConn2, ClientAddr2 = sk.accept()
    print("Channal2 connect from ", ClientAddr2)

    innoServer.SetResponseConn(ClientConn2)
    inputs.append(ClientConn2)
    # thd = threading.Thread(target = handle_client3_request, args = (ClientConn2, ClientAddr2))
    # innoServer.thread.append(thd)
    # thd.setDaemon(True)
    # thd.start()

    # 检查是否受到数据
    while True:

        # 1,需要内核检测哪些链接，有一个活动就返回所有链接循环。
        # 2,处理返回数据。
        # 3,如果有并发的链接断开，内核会返回报错到inputs内，有哪几个有问题。
        # 有链接进入会返回三个数据：
        # readable：返回一个列表，活动的，可读数据的
        # writeable：存放需要返回的数据。
        # exceptional：返回出现异常的活动链接
        readable,writeables,exceptional = select.select(inputs,outputs,inputs)
        print(readable,writeables,exceptional)

        # inputs收处理
        for s in readable:
            if s is sk:
                # 可读的套接字需要准备好接收连接。
                connection, client_address = s.accept()
                print('connection from', client_address, file=sys.stderr)
                connection.setblocking(0)
                inputs.append(connection)

            # 获取数据
            else:
                data = s.recv(1024)

                if data:
                    # 打印数据
                    print("{}收到数据:".format(s.getpeername()),data)
                else:
                    inputs.remove(s)
                    s.close()

        # 删除：错误链接
        for e in exceptional:
            # 删除inputs下的错误链接
            inputs.remove(e)
            s.close()

        if not inputs:
            print("connection all release")
            break


def Unsolicated(data):
    global innoServer
    innoServer.Conn["Unsolicated"].send(data)

def Response(data):
    global innoServer
    innoServer.CurrespConn.send(data)


if __name__ == '__main__':
    InnoServerMain()
