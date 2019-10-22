"""
@Author: 邓润庭
@Date:   2019/10/13
"""
import execjs

# 直接使用js中的函数
ret = execjs.eval("'red yellow green'.split(' ')")
print(ret)

# 因为此时在node的环境中运行，因此不会打印在python环境的终端
execjs.eval("console.log('Hellow World!')")
