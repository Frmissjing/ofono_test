#!/usr/bin/python3
import os
import sys
import pathlib
import importlib
import server_api
import subprocess
import signal
import time
import shlex

global ofono_Terminator,trace_fd
global dirlist 
dirlist = {"case", "common"}


def run_ofono():
    global ofono_Terminator,dirlist

    cmd = shlex.split("./ofonod -nd '*'")
    trace_dir = "./trace/"
    trace_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    print(trace_name)
    trace_fd = open("{}{}.txt".format(trace_dir,trace_name), 'a')
    ofono_Terminator = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd="/home/dreamhigh/code/ofono_vs/ofono/src/")
    ofono_Terminator.wait(3)
    # ofono_Terminator = subprocess.Popen("./ofonod -nd '*'",stdout=trace_fd, shell=True, cwd="/home/dreamhigh/code/ofono_vs/ofono/src/")
    print("{}: pid={}".format(sys._getframe().f_code.co_name,ofono_Terminator.pid))


def run_server():
    pass

def close_ofono():
    global ofono_Terminator
    global trace_fd

    if ofono_Terminator != None:
        print("{}: pid={}".format(sys._getframe().f_code.co_name,ofono_Terminator.pid))
        os.kill(ofono_Terminator.pid, signal.SIGTERM)

    if trace_fd != None:
        trace_fd.close()

def close_server():
    pass



def test_init():
    #启动Ofono
    run_ofono()
    #启动server
    run_server()
    

def test_deinit():
    #关闭Ofono
    close_ofono()
    #关闭server
    close_server()


def add_sys_path():
    global dirlist
    path = os.getcwd()
    for dir in dirlist:
        path1 = "{}/{}".format(path, dir)
        print(path1)
        sys.path.append(path1)

def seek_files(name):
    """根据输入的文件名称查找对应的文件夹有无改文件，有则输出文件地址"""
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

def run_case(filename):
    ret = importlib.import_module(filename)
    eval("ret.{}".format(filename))()    

if __name__ == "__main__":
    #add path 
    add_sys_path()

    casename = input("请输入需要运行的case名称:")
    filename = "{}.py".format(casename)

    # 查找casetest
    filepath = seek_files(filename)

    #启动ofono 

    if filename != None:
        run_case(casename)
    else:
        print("not find file")




