import psycopg2
import psycopg2.extras

# conn = psycopg2.connect("dbname=test_db user=postgres password=password host=10.211.55.3")


class Psycopg2BaseUsage(object):

    def __init__(self,
                 host='localhost',
                 port=5432,
                 user='user',
                 password='passwd',
                 dbname='dbname'):
        # 连接到数据库
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        print("已建立数据库连接")

    def create_table(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def drop_table(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def insert(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
        self.connection.commit()

    def select_all(self, sql, params=None):
        results = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
        return results

    def select_many(self, sql, params=None, size=1):
        results = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchmany(size)
        return results

    def select_one(self, sql, params=None):
        result = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
        return result

    def __del__(self):
        self.connection.close()
        print("已断开数据库连接")


if __name__ == '__main__':
    obj = Psycopg2BaseUsage(host="192.168.219.3", user="postgres", password="passwd", dbname="test_db")
    # 建表语句
    create_sql = '''
        CREATE TABLE if not exists test_table (
            id serial NOT NULL,
            colume1 varchar(255) NOT NULL,
            colume2 varchar(255) NOT NULL,
            PRIMARY KEY (id)
        );'''
    obj.create_table(create_sql)

    # 删表语句
    # drop_sql = '''DROP TABLE test_table'''
    # obj.drop_table(drop_sql)

    # 插入数据
    # insert_sql = "INSERT INTO test_table (colume1, colume2) VALUES (%s, %s)"
    # obj.insert(insert_sql, ("data1", "data2"))

    # 查询数据
    select_sql = "SELECT * FROM test_table"
    results = obj.select_all(select_sql)
    print("all: ", results)
    print(results[0]["id"])
    #
    # results = obj.select_many(select_sql, size=10)
    # print("many: ", results)
    #
    # result = obj.select_one(select_sql)
    # print("one: ", result)
