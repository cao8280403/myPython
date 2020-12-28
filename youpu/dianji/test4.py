import os
import sys
import string
import psutil
import time


def get_pid(name):
    # a = psutil.users()
    process_list = list(psutil.process_iter())
    pids = []
    pids2 = []
    for p in process_list:
        try:
            # print(p.pid)
            # print(p._create_time)
            # print(p._name)
            # print(p.username())
            # print(str(p))
            if p.name()=="cmd.exe":
                pids.append(p)
            if p.name()=="conhost.exe":
                pids2.append(p)
            # if p.name() == "WeChat.exe" and p.create_time() + 5 * 60 < time.time():
            #     pids.append(p.pid)
            # ini_regex = re.compile(regex)
            # result = ini_regex.search(process_info)
            # if result != None:
            #     pid = string.atoi(result.group(1))
            #     print(result.group())
            #     break
        except Exception as error:
            print("error 5: " + str(error))
    print(len(pids))
    for a in pids:
        print(str(a))
    for a in pids2:
        print(str(a))
    pids2.sort(key=lambda x: x.create_time())
    for a in pids2:
        print(str(a))
    pids3 = pids2[3:]
    print("pids3")
    for a in pids3:
        print(str(a))
    #     os.system('taskkill /pid '+str(a)+' /f')
    #     # os.system('taskkill /pid WeChatWeb.exe /f')

def main(argv):
    name = 5544
    print(time.time())
    get_pid(name)

if __name__ == "__main__":
    main(sys.argv)
