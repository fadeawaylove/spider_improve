"""
@Author: 邓润庭
@Date:   2019/10/13
"""
import execjs

js_code = """
function f(temp){
    console.log(temp);
    return temp
}
"""

# 先编译
js_context = execjs.compile(js_code)
# 然后调用定义的函数
ret = js_context.call("f", "我是你爸爸!")
print(ret)
