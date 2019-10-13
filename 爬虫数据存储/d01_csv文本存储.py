"""
@Author: 邓润庭
@Date:   2019/10/13
"""
import csv  # Python内置模块

col1 = ["col1-data1", "col1-data2", "col1-data3"]
col2 = ["col2-data1", "col2-data2", "col2-data3"]

with open("test.csv", "w") as file:
    # 定义writer对象
    writer = csv.writer(file)
    # 先在第一行写入列名称
    writer.writerow(["第一列", "第二列"])
    # 利用writerows一次写入多行数据
    rows = list(zip(col1, col2))
    '''rows:
    [('col1-data1', 'col2-data1'),
    ('col1-data2', 'col2-data2'),
    ('col1-data3', 'col2-data3')]
    '''
    writer.writerows(rows)

# 查看是否写入成功
import os

os.system("cat test.csv")
'''运行结果
第一列,第二列
col1-data1,col2-data1
col1-data2,col2-data2
col1-data3,col2-data3
'''
