from socket import *
import sys,os


def send_msg(s, name, ADDR):
    while True:
        text = input('')
        if text.strip() == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(), ADDR)
            sys.exit('退出聊天室')

        msg = 'C %s %s' % (name, text)
        s.sendto(msg.encode(), ADDR)

def recv_msg(s):
    while True:
        data, addr = s.recvfrom(2048)
        if data.decode() == 'EXIT':
            sys.exit(0)
        print(data.decode())

# 创建套接字。登录。创建子进程
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)
    # 创建套接字
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input('请输入姓名:')
        msg = 'L ' + name
        # 发送登录请求
        s.sendto(msg.encode(), ADDR)
        data, addr = s.recvfrom(1024)
        if data.decode() == 'ok':
            print('您进入了聊天室')
            break
        else:
            print(data.decode())
    # 创建父子进程
    pid = os.fork()
    if pid < 0:
        sys.exit('创建子进程失败')
    elif pid == 0:
        send_msg(s, name, ADDR)
    else:
        recv_msg(s)


if __name__ == '__main__':
    main()
