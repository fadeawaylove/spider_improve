"""
@Author: 邓润庭
@Date:   2019/10/13
"""
import js2py

# 前提：先安装好nodejs，并使用 npm install crypto-js 安装
# crypto-js是node中数据加密、解密算法库

# 获取nodejs中环境中安装的crypto-js模块
CryptoJS = js2py.require('crypto-js')
data = [{'data1': "hello world"}, {'data2': 666}]
JSON = js2py.eval_js('JSON')  # 获取js中的JSON对象
ciphertext = CryptoJS.AES.encrypt(JSON.stringify(data), 'secret key 123')
print("ciphertext: ", ciphertext)
bytes = CryptoJS.AES.decrypt(ciphertext.toString(), 'secret key 123')
print("bytes: ", bytes)
decryptedData = JSON.parse(bytes.toString(CryptoJS.enc.Utf8)).to_list()
print("decryptedData: ", decryptedData)

'''运行结果
v8.11.4
npm WARN deprecated babel-preset-es2015@6.24.1: 🙌 Thanks for using Babel: we recommend using babel-preset-env now: please read babeljs.io/env to update! 
...
...
...如果出现以上信息，属于正常，因为js2py模块中使用的一个库babel-preset-es2015，被node遗弃了，所以出现这个警告

ciphertext: {'$super': {......
bytes: {'sigBytes': 39, 'words': [1534796388,......
decryptedData: [{'data1': 'hello world'}, {'data2': 666}]
'''
