#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-

import subprocess
import threading
import time
import sys
import os
import paramiko
import warnings
warnings.filterwarnings("ignore")

global cliinput
global stdin
global stdout
global stderr

cliinput=[]
stdout=classmethod
lock = threading.Lock()

sys.argv

def inputcli():
    clilist = ['hostname']
    clilist.append(sys.argv[2])
    return  clilist

"""
    clistr = ",".join(clilist)
    clistr.split(',')

    cli_str = ""
    for cli in clistr.split(','):
        cli = "'"+cli+"'"
        cli_add = cli.encode('utf8')
        cli_str = cli_str + ',' + cli_add
    cli_str = cli_str[1:]
    return cli_str
"""


def sshnode(ip,username,password,args):
    x = 10000
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    time.sleep(0.1)
    ssh.connect(ip,22,username,password)
    #print args

    for index,one_cli in enumerate(args):
        #cmd = one_cli
        #ssh.exec_command(cmd)
        lock.acquire()
        try:
            cmd = one_cli
            ssh.exec_command(cmd)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            if not result:
                result = stderr.read()
            print result.decode()
        finally:
            lock.release()
    ssh.close()
#sshnode('localhost','cyy','echo@520277',inputcli())


def getdata(name,ip,username,password):
    #print type(ip)
    #print type(username)
    #print type(password)
    #print type(cliinput)
    ##cmd = sshnode(ip,username,password,cliinput)
   # print name
    sshnode(ip,username,password,cliinput)
    #os.exec(cmd)
#    result1 = run_cmd.stdout.read()
#    run_cmd = subprocess.Popen("id", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#    result2 = run_cmd.stdout.read()
#    print "="*20
#    print result1
#    print result2
#    print "="*20
    return


def readcfg(p):
    cfgList = []
    with open(p,'r') as f:
        lineList = f.readlines()
    for line in lineList:
        if len(line.strip()) == 0 or line.strip()[0] == "#":
            continue
        cfgList.append(line)
    return cfgList



def banner():
    nodetype = str(sys.argv[1])
    #nodetype = sys.argv[0]
    #print(sys.argv[1])
    if nodetype == 'cg':
        node ='./cg.cfg'
    elif nodetype == 'mme':
        node ='./mme.cfg'
    elif nodetype == 'saegw':
        node ='./saegw.cfg'
    elif nodetype == 'pcrf':
        node ='./pcrf.cfg'
    else:
        sys.exit()
    return node

def dothreading(node):
    threads = []
    for msg in readcfg(node):
        msgList = msg.split()
        name,ip,username,password = msgList[0],msgList[1],msgList[2],msgList[3]
    	t = threading.Thread(target=getdata,args=(name,ip,username,password))
        #t.run()
    	threads.append(t)
        #result = stdout.read()
        #if not result:
        #    result = stderr.read()
        #print(result.decode())
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        #print t.get_result()

def main():
    #actioncmd = 'ls'
    global cliinput
    #print cliinput
    node = banner()
    cliinput = list(inputcli())
    st = time.time()
    dothreading(node)
    et = time.time()
    #print "%sFinished [run time: %.2f]" % ( "-" * 40, et - st)

main()
