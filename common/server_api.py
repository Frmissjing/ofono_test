'''
Author: Frmissjing 892153623@qq.com
Date: 2023-11-22 18:15:08
LastEditors: Frmissjing 892153623@qq.com
LastEditTime: 2023-11-24 16:22:05
FilePath: /ofono_test/common/server_api.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
#!/usr/bin/python3
import socket
# 导入线程模块
import threading

global innoServer
global Buff1,Buff2,buff3

class InnoServer(object):
    'InnoServer'
    Conn = {}
    CurrespConn = None
    thread = []

    def __init__(self):
        # 创建服务端套接字对象
        self.ServerSk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # 设置端口复用，程序退出后端口马上释放
        self.ServerSk.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    
        # 绑定端口
        self.ServerSk.bind(("",12345))
    
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
            print("客户端发来的消息是:", recv_data.decode())
            buff1.apepend(recv_data.decode())


# 接收下发通道数据
def handle_client3_request(conn, addr):
    global buff3
    # 循环接收数据
    while True:
        recv_data = conn.recv(4096)
        
        # 如果接收到数据，就村到buff
        if recv_data:
            print("客户端是:", addr)
            print("客户端发来的消息是:", recv_data.decode())
            buff3.apepend(recv_data.decode())


def InnoServerMain():
    global innoServer
    # 创建InnoServer
    innoServer = InnoServer()
    
    # 等待第一个Client连接(通道1，下发通道1)
    ClientConn1, ClientAddr1 = innoServer.GetSocket.accept()
    innoServer.SetResponseConn(ClientConn1)
    # 创建线程对象,将接收到的数据存到buff
    thd = threading.Thread(target = handle_client1_request, args = (ClientConn1, ClientAddr1))
    innoServer.thread.append(thd)
    thd.setDaemon(True)
    thd.start()

    # 等待第二个Client连接(通道2,主动上报通道)
    ClientConn, ClientAddr = innoServer.GetSocket.accept()
    innoServer.SetResponseConn(ClientConn)

    while True:
        # 等待第三个Client连接(通道3,下发通道2)
        ClientConn2, ClientAddr2 = innoServer.GetSocket.accept()
        innoServer.SetResponseConn(ClientConn2)
        thd = threading.Thread(target = handle_client3_request, args = (ClientConn2, ClientAddr2))
        innoServer.thread.append(thd)
        thd.setDaemon(True)
        thd.start()



def Unsolicated(data):
    innoServer.Conn["Unsolicated"].send(data)

def Response(data):
    innoServer.CurrespConn.send(data)



# 定义个函数,使其专门重复处理客户的请求数据（也就是重复接受一个用户的消息并且重复回答，直到用户选择下线）
def dispose_client_request(tcp_client_1,tcp_client_address):
    # 5 循环接收和发送数据
    while True:
        recv_data = tcp_client_1.recv(4096)
        
        # 6 有消息就回复数据，消息长度为0就是说明客户端下线了
        if recv_data:
            print("客户端是:", tcp_client_address)
            print("客户端发来的消息是:", recv_data.decode())
            send_data = "消息已收到，正在处理中...".encode()
            tcp_client_1.send(send_data)
        else:
            print("%s 客户端下线了..." % tcp_client_address[1])
            tcp_client_1.close()
            break

if __name__ == '__main__':

    # 1 创建服务端套接字对象
    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
  
    # 2 绑定端口
    tcp_server.bind(("",12345))
  
    # 3 设置监听
    tcp_server.listen(128)
    
    # 4 循环等待客户端连接请求（也就是最多可以同时有128个用户连接到服务器进行通信）
    while True:
        tcp_client_1 , tcp_client_address = tcp_server.accept()
        # 创建多线程对象
        thd = threading.Thread(target = dispose_client_request, args = (tcp_client_1,tcp_client_address))
        
        # 设置守护主线程  即如果主线程结束了 那子线程中也都销毁了  防止主线程无法退出
        # thd.setDaemon(True)
        
        # 启动子线程对象
        thd.start()

    # 7 关闭服务器套接字 （其实可以不用关闭，因为服务器一直都需要运行）
    # tcp_server.close()

