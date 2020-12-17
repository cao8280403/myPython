from sqlalchemy import Column, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

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


# 定义User对象:
class Cookie(Base):
    # 表的名字:
    __tablename__ = 'cookie'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    cookie = Column(String(20))
    # 一对多:
    vvs = relationship('Vv')

class Vv(Base):
    # 表的名字:
    __tablename__ = 'vv'

    # 表的结构:
    guid = Column(String(225), primary_key=True)
    columna = Column(String(225))
    columnb = Column(String(225))
    juid = Column(String(225))
    postaga = Column(String(225))
    # postagb = Column(String(225))
 # “多”的一方的book表是通过外键关联到user表的:
    postagb = Column(String(20), ForeignKey('cookie.id'))




# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:Youpu123@localhost:3306/youpudb')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 创建session对象:
# session = DBSession()
# # 创建新User对象:
# new_user = Vv(guid='345', columna='Bo334b')
# # 添加到session:
# session.add(new_user)
# # 提交即保存到数据库:
# session.commit()
# # 关闭session:
# session.close()

# 创建Session:
# session = DBSession()
# # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
# user = session.query(Cookie).filter(Cookie.id=='5').one()
# # 打印类型和对象的name属性:
# # print 'type:', type(user)
# # print 'name:', user.name
# print(user.vvs)
# # 关闭Session:
# session.close()

session = DBSession()
ua_all = session.query(Ua).all()
for i in ua_all:
    print(i.content)
session.close()