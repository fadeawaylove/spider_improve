"""
@Author: 邓润庭
@Date:   2019/10/13
"""
import js2py

js_code = """
pyimport requests
console.log("导入成功！");

var response = requests.get("http://wwww.baidu.com");
console.log(response.url);
console.log(response.content);
"""

js2py.eval_js(js_code)
