"""
@Author: 邓润庭
@Date:   2019/10/12
"""
import js2py

print("sum: {}".format(sum([1, 2, 3])))

context = js2py.EvalJs({"python_sum": sum})

print("context.python_sum: {}".format(context.python_sum))

js_code = """
python_sum([1,2,3])
"""
print("js_code运行结果: {}".format(context.eval(js_code)))
