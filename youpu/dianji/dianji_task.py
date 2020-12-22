from sqlalchemy import Column, String, create_engine, ForeignKey, func
from fetchip import Fetchip
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from db_class import Mipcms_fabao_history, Mipcms_fabao, City_cookies
from aliip import Aliip
from dianji_thread import Dianji_thread
import time
from open_chrome import oneThread


g_ids = []

class Aclass(object):
    def __init__(self):
        self.fabaos = []
        self.citycookies = []

    def fetch_fabao(self):
        cursor = session.execute(
            "select a.* from (select * from mipcms_fabao_history where time > UNIX_TIMESTAMP(date_format(now(),'%Y-%m-%d'))) a  left join mipcms_fabao b on a.site = b.site and a.keyword=b.keyword and a.count<b.mubiao order by rand()")
        result = cursor.fetchall()
        print(len(result))
        self.fabaos = result

    def fetch_cookies(self):
        citycookies = session.query(City_cookies).all()
        print(len(citycookies))
        self.citycookies = citycookies


if __name__ == '__main__':
    print("begin process")
    try:
        engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()  # 创建session
        aclass = Aclass()
        aclass.fetch_cookies()
        while True:
            aclass.fetch_fabao()
            if len(aclass.fabaos) > 0 and len(aclass.fabaos[0]) > 0:
                time.sleep(1)
                # aclass.fabaos.pop(0)
                obj_fetchip = Fetchip()
                ips = obj_fetchip.requesturl()
                threads = []
                for ip in ips:
                    if len(aclass.fabaos) > 0:
                        fabaos_one = aclass.fabaos.pop(0)
                        fabaos_two = ""
                        site = fabaos_one["site"]
                        for word in aclass.fabaos:
                            if word["site"] == site:
                                word_two = aclass.fabaos.pop(aclass.fabaos.index(word))
                                break
                        one = oneThread(fabaos_one, fabaos_two, site,
                                        "--proxy-server=http://" + ip["ip"] + ":" + ip["port"], ip["ip"], aclass.citycookies)
                        threads.append(one)
                for thread in threads:
                    thread.start()
                print("threads")
            else:
                print("fetchdb")
                aclass.fetch_fabao()
    except Exception as err:
        print(err)
print("end process")
