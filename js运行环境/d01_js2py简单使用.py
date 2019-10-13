"""
@Author: 邓润庭
@Date:   2019/10/12
"""
import js2py

js2py.eval_js("console.log('Hello World!')")

func_js = """
function add(a, b){
    return a + b
}
"""

add = js2py.eval_js(func_js)
print(add(1, 12))
print(add.constructor)
