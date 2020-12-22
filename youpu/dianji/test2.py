import random

import MySQLdb
import time
print(time.time())

conn =  MySQLdb.connect(host='192.168.1.10', port=3306, user='youpudb', password='Youpu123', database='youpudb',
                               charset='utf8')
try:
    with conn.cursor() as cursor:
        for i in range(10):
        	# 定义列表参数
            params = []
            for j in range(1, 101):
                username = f'user{100 * i + j}'
                password = '877'
                params.append((username, password))
            cursor.executemany(
                'insert into tb_user (username, password) values (%s, %s)',
                params # 此处从一个单元组编程了包含多个元组的列表
            )
    # 4. 提交事务
    conn.commit()
except MySQLdb.MySQLError as err:
    print(err)
    # 4. 回滚事务
    conn.rollback()
finally:
    # 5. 关闭数据库连接（释放资源）
    conn.close()