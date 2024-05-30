#!/usr/bin/python3
import os
import sys
import pathlib
import importlib
import subprocess
import signal
import time
import shlex
import traceback
import threading
import server_api

global ofonoProcess,trace_fd
global dirlist 
dirlist = {"case", "common"}


'''
description: 添加python脚本运行的lib路径和case路径
return {*}
'''
def add_sys_path():
    global dirlist
    path = os.getcwd()
    for dir in dirlist:
        path1 = "{}/{}".format(path, dir)
        print(path1)
        sys.path.append(path1)



'''
description: 启动ofono应用程序
param {*} CaseName case名称
return {*}
'''
def run_ofono(CaseName):
    global ofonoProcess, trace_fd, dirlist
    # 启动命令
    cmd = shlex.split("./ofonod -nd '*'")
    # 设置trace路径和名称
    trace_dir = "./trace"
    trace_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    # 启动ofono，并将ofono的trace打印到tarce目录
    with open("{}/{}_{}.txt".format(trace_dir, CaseName, trace_name), 'a') as trace_fd:
        ofonoProcess = subprocess.Popen(cmd, stdout=trace_fd, stderr=trace_fd, cwd="/home/dreamhigh/code/ofono_vs/ofono/src/")
    print("{}: pid={}".format(sys._getframe().f_code.co_name,ofonoProcess.pid))


'''
description: 
return {*}
'''
def close_ofono():
    global ofonoProcess
    global trace_fd

    if ofonoProcess != None:
        print("{}: pid={}".format(sys._getframe().f_code.co_name, ofonoProcess.pid))
        os.kill(ofonoProcess.pid, signal.SIGINT)

    if trace_fd != None:
        print("{}: file {} closed.".format(sys._getframe().f_code.co_name, trace_fd.name))
        trace_fd.close()

'''
description: 启动脚本的server
return {*}
'''
def InitInnoServer():
    # 创建Innoserver线程
    innoServer = server_api.InnoServer()
    pass

'''
description: 启动脚本的server
return {*}
'''
def run_server():
    # 创建Innoserver线程
    InnoServerThd = threading.Thread(target = InitInnoServer)


'''
description: 
return {*}
'''
def close_server():
    pass



'''
description: 脚本初始化:启动ofono和server
param {*} filename 运行的case名称
return {*}
'''
def test_init(filename):
    #启动Ofono
    run_ofono(filename)
    #启动server
    run_server()
    
'''
description: 
return {*}
'''
def test_deinit():
    #关闭Ofono
    close_ofono()
    #关闭server
    close_server()


'''
description: 
param {*} name
return {*}
'''
def seek_files(name):
    """根据输入的文件名称查找对应的文件夹有无该文件，有则输出文件地址"""
    path = os.getcwd()
    print(path)
    path = "{}/{}".format(path,"case")
    print(path)
    print(name)
    for root, dirs, files in os.walk(path):
        print(files)
        if name in files:
            # 当层文件内有该文件，输出文件地址
            filepath = '{0}/{1}'.format(root, name)
            print(filepath)
            return filepath
    return None


'''
description: 
param {*} filename
return {*}
'''
def run_case(filename):
    ret = importlib.import_module(filename)
    try:
        # 启动ofono 和 server
        test_init(filename)
        # dealy 3s
        time.sleep(3)
        # 运行case
        eval("ret.{}".format(filename))()
    except Exception as e:
        traceback.print_exc()
    
    #case结束，关闭ofono和server
    test_deinit()


'''
description: 
return {*}
'''
if __name__ == "__main__":
    #add path 
    add_sys_path()

    casename = input("请输入需要运行的case名称:")
    filename = "{}.py".format(casename)

    # 查找case
    filepath = seek_files(filename)

    if filename != None and os.path.isfile(filepath):
        run_case(casename)
    else:
        print("not find file")




