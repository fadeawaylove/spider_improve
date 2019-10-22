"""
@Author: 邓润庭
@Date:   2019/10/14
"""
import pymysql


class MysqlConn(object):
    """上下文管理器实现连接池对象"""

    def __init__(self, **mysql_config):
        self.connection = pymysql.connect(**mysql_config, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print("执行事务时候出错，准备回滚！")
            self.connection.rollback()
        else:
            print("事务执行成功，准备提交事务！")
            self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor


if __name__ == '__main__':
    mysql_config_dict = dict(
        host='192.168.219.3', port=3306, user='root', password='mysql', db='test_db'
    )
    with MysqlConn(**mysql_config_dict) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS `test_table` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `colume1` varchar(255) NOT NULL,
            `colume2` varchar(255) NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
        AUTO_INCREMENT=1;"""
        )

    # with MysqlConn(**mysql_config_dict) as conn:
    #     conn.execute("insert into test_table(colume1, colume2) values(%s, %s)", ["嘿嘿嘿", "哈哈哈"])
    #     raise Exception("aaaaa")
    #     ret = conn.execute("select * from test_table").fetchmany(10)
    #     print(ret)

    with MysqlConn(**mysql_config_dict) as conn:
        ret = conn.execute("select * from test_table").fetchmany(10)
        print(ret)
