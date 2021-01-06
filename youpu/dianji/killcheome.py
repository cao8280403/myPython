import time
import json
import os
import psutil

def close_chrome():
    try:
        process_list = list(psutil.process_iter())
        pids = []
        cmd_pids = []
        conhost_pids = []
        for p in process_list:
            if p.name() == "chrome.exe" and p.create_time() + 5 * 60 < time.time():
                pids.append(p.pid)
            if p.name() == "cmd.exe":
                cmd_pids.append(p)
            if p.name() == "conhost.exe":
                conhost_pids.append(p)
        print("close pids count:" + str(len(pids)))
        for pid in pids:
            try:
                os.system('taskkill /pid ' + str(pid) + ' /f')
            except Exception as error:
                print("error 2: " + str(error))
        cmd_pids.sort(key=lambda x: x.create_time())
        conhost_pids.sort(key=lambda x: x.create_time())
        cmd_pids2 = cmd_pids[6:]
        conhost_pids3 = conhost_pids[8:]
        for pid in cmd_pids2:
            try:
                os.system('taskkill /pid '+str(pid.pid)+' /f')
            except Exception as error:
                print("error 3: " + str(error))
        for pid in conhost_pids3:
            try:
                os.system('taskkill /pid '+str(pid.pid)+' /f')
            except Exception as error:
                print("error 4: " + str(error))
    except Exception as error:
        print("error 5: " + str(error))



if __name__ == '__main__':
    try:
        while True:
            close_chrome()
            time.sleep(60)
    except Exception as err:
        print("error 1: " + str(err))
print("end process")
