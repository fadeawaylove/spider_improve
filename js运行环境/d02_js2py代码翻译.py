"""
@Author: 邓润庭
@Date:   2019/10/12
"""
import js2py

print(js2py.translate_js("console.log('Hello World!')"))


# 将js翻译成python代码
js2py.translate_file('d02.js', 'd02.py')
