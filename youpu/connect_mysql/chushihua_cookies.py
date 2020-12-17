#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column, String, create_engine, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from fetchip import Fetchip
from aliip import Aliip
from getali_thread import Getali_thread
import threading
import time

# 创建对象的基类:
Base = declarative_base()


class City_cookies(Base):
    __tablename__ = 'city_cookies'
    id = Column(String(255), primary_key=True)
    cookie = Column(String(255))
    city = Column(String(255))
    zone = Column(String(255))
    ua = Column(String(255))


class Ua(Base):
    __tablename__ = 'ua'
    content = Column(String(255), primary_key=True)


if __name__ == '__main__':
    print("begin process")
    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:Youpu123@localhost:3306/youpudb')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()  # 创建session
    # 查出所有的cookie 依次给他赋值 最后保存
    # objs = session.query(City_cookies).filter(City_cookies.ua.isnot(None)).limit(10).all()
    while True:
        uas = session.query(Ua).order_by(func.random()).limit(200).all()
        city_cookies = session.query(City_cookies).filter(City_cookies.ua == None).limit(len(uas)).all()
        if len(city_cookies) == 0:
            break
        obj_fetchip = Fetchip()
        ips = obj_fetchip.requesturl()
        threads = []
        results = []
        for i in range(len(city_cookies)):
            getali_thread = Getali_thread(ips[i]["origin_ip"])
            threads.append(getali_thread)

        for tmp in threads:
            tmp.start()

        for tmp in threads:
            tmp.join()
            results.append(tmp.getResult())

        for i in range(min(len(uas),len(city_cookies)) ):
            city_cookies[i].city = results[i]["City"]
            city_cookies[i].zone = results[i]["County"]
            city_cookies[i].ua = uas[i].content

        save_objs = [{'id': obj.id, 'cookie': obj.cookie, 'city': obj.city, 'zone': obj.zone, 'ua': obj.ua} for obj in
                     city_cookies]
        session.bulk_update_mappings(City_cookies, save_objs)
        session.commit()

    print("end process")
