"""
@Author: 邓润庭
@Date:   2019/10/13
"""
import execjs

default_runtime = execjs.get()
print(default_runtime)
print(default_runtime.name)

import execjs.runtime_names

node = execjs.get(execjs.runtime_names.Node)
print(node)
print(node.name)
