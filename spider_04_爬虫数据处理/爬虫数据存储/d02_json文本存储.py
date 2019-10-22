"""
@Author: 邓润庭
@Date:   2019/10/13
"""
'''利用json模块将python列表或字典装换为json字符串，再写入'''
import json

json_data = [
    {"firstName": "Bill", "lastName": "Gates"},
    {"firstName": "George", "lastName": "Bush"},
    {"firstName": "Thomas", "lastName": "Carter"}
]
with open("test.json", "w") as file:
    file.write(json.dumps(json_data, indent=2))  # indent控制json字符串的缩进，使得结构更美观

import os

os.system("cat test.json")
'''运行结果
[
  {
    "firstName": "Bill",
    "lastName": "Gates"
  },
  {
    "firstName": "George",
    "lastName": "Bush"
  },
  {
    "firstName": "Thomas",
    "lastName": "Carter"
  }
]
'''
