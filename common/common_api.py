#!/usr/bin/python3
import server_api
import subprocess
import os
import signal
import time
import shlex
import sys

global ofono_Terminator,trace_fd

def run_ofono():
    global ofono_Terminator
    global trace_fd

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

    pass


if __name__ == "__main__":
    test_init()
    time.sleep(5)
    test_deinit()

