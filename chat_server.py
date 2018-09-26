#!/user/bin/env python3
# coding = utf-8

from socket import *
import os,sys
# 登陆判断
def do_login(s, user, name, addr):
    if (name in user) or (name == '管理员'):
        s.sendto('该姓名已存在'.encode(), addr)
        return
    else:
        s.sendto(b'ok', addr)
        #通知其他人
        msg = '欢迎 %s 进入聊天室' % name
        for i in user:
            s.sendto(msg.encode(), user[i])
        # 插入用户
        user[name] = addr

def do_chat(s, user, name, text):
    msg = '%s: %s' % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])

def do_quit(s, user, name):
    msg = name + '退出了聊天室'
    for i in user:
        if i == name:
            s.sendto(b'EXIT', user[i])
        else:
            s.sendto(msg.encode(), user[i])
    del user[name]

# 接收客户端请求
def do_parent(s):
    user = {}
    #print('22222')
    while True:
        msg, addr = s.recvfrom(1024)
        msglist = msg.decode().split(' ')
        if msglist[0] == 'L':
            do_login(s, user, msglist[1], addr)
        elif msglist[0] == 'C':
            do_chat(s, user, msglist[1], ' '.join(msglist[2:]))
        elif msglist[0] == 'Q':
            do_quit(s, user, msglist[1])

# 管理员
def do_child(s, addr):
    # print('1111')
    while True:
        msg = input('管理员消息:')
        msg = 'C 管理员 ' + msg
        s.sendto(msg.encode(), addr)

def main():
    addr = ('0.0.0.0', 3344)

    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(addr)

    # 创建一个新的进程处理管理员喊话功能
    pid = os.fork() 
    if pid < 0:
        sys.exit('创建失败')
    elif pid == 0:
        do_child(s, addr)
    else:
        do_parent(s)

if __name__ == '__main__':
    main()