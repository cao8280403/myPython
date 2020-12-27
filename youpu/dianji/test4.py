import os
import sys
import string
import psutil
import time


def get_pid(name):
    process_list = list(psutil.process_iter())
    pids = []
    for p in process_list:
        # print(p.pid)
        # print(p._create_time)
        # print(p._name)
        # print(str(p))
        if p.name()=="WeChat.exe" :
            pids.append(p.pid)

        # ini_regex = re.compile(regex)
        # result = ini_regex.search(process_info)
        # if result != None:
        #     pid = string.atoi(result.group(1))
        #     print(result.group())
        #     break
    print(len(pids))
    for a in pids:
        print(str(a))
        os.system('taskkill /pid '+str(a)+' /f')
        # os.system('taskkill /pid WeChatWeb.exe /f')

def main(argv):
    name = 5544
    print(time.time())
    get_pid(name)

if __name__ == "__main__":
    main(sys.argv)