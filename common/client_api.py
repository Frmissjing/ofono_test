#!/usr/bin/python3
import socket
# 导入线程模块
import threading

def inno_client_creat_channel():
    host = '127.0.0.1'
    port = 12345
    addr = (host, port)
    # 创建socket对象
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    # 连接目标主机
    s.connect(addr)
    return s

def unsol_channel_rcv(s):
    while True:
        try:
            data = s.recv(2048)
            if data:
                # 接收到的数据数据
                print("unsol_channel_rcv recv data:}", data.decode('utf8'))
        except Exception:
            break
                


def main():
    # 创建channel1
    s_channel1 = inno_client_creat_channel()

    # 创建unsol_channel
    s_unsol_channel = inno_client_creat_channel()

    # 创建接收主动上报线程
    p = threading.Thread(target=unsol_channel_rcv, args=(s_unsol_channel))
    p.start()

    # 创建channel2
    s_channel2 = inno_client_creat_channel()

    while True:
        
        # channel1 发送数据和接受响应
        data = input("请输入Channel1发送的数据:")
        s_channel1.sendall(data.encode('utf8'))

        # channel1 发送数据和接受响应
        data = input("请输入Channel2发送的数据:")
        s_channel2.sendall(data.encode('utf8'))

if __name__ == '__main__':
    main()
