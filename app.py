from flask import Flask, render_template, request, jsonify
import hashlib
import reply
import receive
import logging
import sys
import xml.dom.minidom
from menu import WeChatMenu

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)
logger = logging.getLogger(__name__)

# 微信公众号配置
WECHAT_APPID = "your_appid"  # 替换为你的APPID
WECHAT_APPSECRET = "your_appsecret"  # 替换为你的APPSECRET

def format_xml(xml_string):
    """格式化 XML 字符串，使其更易读"""
    try:
        dom = xml.dom.minidom.parseString(xml_string)
        return dom.toprettyxml(indent="  ")
    except:
        return xml_string

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_menu', methods=['POST'])
def create_menu():
    """创建自定义菜单"""
    try:
        menu = WeChatMenu(WECHAT_APPID, WECHAT_APPSECRET)
        if menu.create_menu():
            return jsonify({"success": True, "message": "创建菜单成功"})
        else:
            return jsonify({"success": False, "message": "创建菜单失败"})
    except Exception as e:
        logger.error(f"创建菜单异常: {str(e)}")
        return jsonify({"success": False, "message": str(e)})

@app.route('/delete_menu', methods=['POST'])
def delete_menu():
    """删除自定义菜单"""
    try:
        menu = WeChatMenu(WECHAT_APPID, WECHAT_APPSECRET)
        if menu.delete_menu():
            return jsonify({"success": True, "message": "删除菜单成功"})
        else:
            return jsonify({"success": False, "message": "删除菜单失败"})
    except Exception as e:
        logger.error(f"删除菜单异常: {str(e)}")
        return jsonify({"success": False, "message": str(e)})

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
        logger.info(f"handle/GET func: hashcode: {hashcode}, signature: {signature}")
        
        # 验证签名
        if hashcode == signature:
            return echostr
        else:
            return ""
            
    except Exception as e:
        logger.error(f"验证失败: {str(e)}")
        return str(e)

@app.route('/wx', methods=['POST'])
def wechat_message():
    try:
        # 获取微信服务器发送的数据
        webData = request.data
        # 格式化 XML 数据并打印日志
        formatted_xml = format_xml(webData.decode('utf-8'))
        logger.info("Handle Post webdata is:\n%s", formatted_xml)
        
        # 解析XML数据
        recMsg = receive.parse_xml(webData)
        
        # 根据消息类型处理不同的消息
        if isinstance(recMsg, receive.Msg):
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            
            # 处理菜单点击事件
            if recMsg.MsgType == 'event' and recMsg.Event == 'CLICK':
                logger.info(f"recMsg.EventKey is {recMsg.EventKey}")
                if recMsg.EventKey == 'zhangtingfenxi':
                    # 处理涨停分析事件
                    content = "正在为您分析涨停数据..."
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                    
                else:
                    logger.info(f"未处理的菜单事件: {recMsg.EventKey}")
                    return "success"
            
            # 处理普通消息
            elif recMsg.MsgType == 'text':
                # 处理文本消息
                content = "您发送了文本消息：" + recMsg.Content
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
                
            elif recMsg.MsgType == 'image':
                # 处理图片消息
                content = "您发送了图片消息，图片链接为：" + recMsg.PicUrl
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
                
            elif recMsg.MsgType == 'voice':
                # 处理语音消息
                content = "您发送了语音消息"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
                
            elif recMsg.MsgType == 'video':
                # 处理视频消息
                content = "您发送了视频消息"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
                
            elif recMsg.MsgType == 'location':
                # 处理位置消息
                content = "您发送了位置消息，位置为：经度 " + str(recMsg.Location_Y) + " 纬度 " + str(recMsg.Location_X)
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
                
            elif recMsg.MsgType == 'link':
                # 处理链接消息
                content = "您发送了链接：" + recMsg.Title
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
                
            else:
                logger.info("暂且不处理")
                return "success"
        else:
            logger.info("暂且不处理")
            return "success"
            
    except Exception as e:
        logger.error(f"处理错误：{str(e)}")
        return str(e)

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=80, debug=True)