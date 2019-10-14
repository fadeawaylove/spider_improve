"""
@Author: 邓润庭
@Date:   2019/10/14
"""
import contextlib
import pymysql
import traceback


@contextlib.contextmanager
def mysql_conn(**mysql_config):
    connection = pymysql.connect(**mysql_config, cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        yield cursor
    except:
        print(traceback.format_exc())
        connection.rollback()
    finally:
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
    mysql_config_dict = dict(
        host='192.168.1.109', port=3306, user='root', password='mysql', db='test_db'
    )
    with mysql_conn(**mysql_config_dict) as conn:
        conn.execute("select * from test_table", [])
        ret = conn.fetchall()
        print(ret)

        conn.execute("insert into test_table(colume1, colume2) values(%s, %s)", ["嘿嘿嘿", "哈哈哈"])

        conn.execute("select * from test_table", [])
        ret = conn.fetchmany(10)
        print(ret)
