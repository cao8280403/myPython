from sqlalchemy import Column, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import time

# 创建对象的基类:
Base = declarative_base()


class Mipcms_fabao_history(Base):
    __tablename__ = 'mipcms_fabao_history'
    id = Column(String(255), primary_key=True)
    site = Column(String(255))
    keyword = Column(String(255))
    time = Column(String(255))
    count = Column(String(255))


class Mipcms_fabao(Base):
    __tablename__ = 'mipcms_fabao'
    id = Column(String(255), primary_key=True)
    site = Column(String(255))
    mubiao = Column(String(255))
    keyword = Column(String(255))


class City_cookies(Base):
    __tablename__ = 'city_cookies'
    id = Column(String(255), primary_key=True)
    cookie = Column(String(255))
    city = Column(String(255))
    zone = Column(String(255))
    ua = Column(String(255))
    error_count = Column(String(255))


class Updatedb():
    def updatedb(self, total_ids):
        print("update db")
        try:
            engine = create_engine('mysql+mysqlconnector://youpudb:Youpu123@192.168.1.10:3306/youpudb')
            # 创建DBSession类型:
            DBSession2 = sessionmaker(bind=engine)
            session2 = DBSession2()  # 创建session
            save_objs = [{'id': obj.id, 'site': obj.site, 'keyword': obj.keyword, 'count': obj.count+1, 'time': obj.time} for obj in
                         total_ids]
            session2.bulk_update_mappings(Mipcms_fabao_history, save_objs)
            session2.commit()
        except Exception as err:
            print(err)
        # conn = MySQLdb.connect(host='192.168.1.10', port=3306, user='youpudb', password='Youpu123', database='youpudb',
        #                        charset='utf8')
        # sql = "INSERT INTO mipcms_fabao_history(`id`,`site`,`keyword`,`time`,`count`) VALUES(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `count`=`count`+1"
        # try:
        #     with conn.cursor() as cursor:
        #         # 定义列表参数
        #         params = []
        #         for i in total_ids:
        #             params.append((i.id, i.site, i.keyword, int(time.time()), i.count))
        #         cursor.executemany(sql, params)  # 此处从一个单元组编程了包含多个元组的列表
        #     # 4. 提交事务
        #     conn.commit()
        # except MySQLdb.MySQLError as err:
        #     print(err)
        #     # 4. 回滚事务
        #     conn.rollback()
        # finally:
        #     # 5. 关闭数据库连接（释放资源）
        #     conn.close()
