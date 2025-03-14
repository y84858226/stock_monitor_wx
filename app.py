from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/wx', methods=['GET'])
def wechat_verify():
    try:
        # 获取参数
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        # 如果是空请求，返回提示信息
        if not all([signature, timestamp, nonce]):
            return "hello, this is handle view"
        
        # 微信公众号配置的token
        token = "huayanh19941229"  # 请替换为您的实际token
        
        # 排序
        temp_list = [token, timestamp, nonce]
        temp_list.sort()
        
        # 拼接字符串并进行sha1加密
        temp_str = ''.join(temp_list)
        sha1 = hashlib.sha1(temp_str.encode('utf-8'))
        hashcode = sha1.hexdigest()
        
        # 打印日志
        print(f"handle/GET func: hashcode: {hashcode}, signature: {signature}")
        
        # 验证签名
        if hashcode == signature:
            return echostr
        else:
            return ""
            
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True) 