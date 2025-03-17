from flask import Flask, render_template, request
import hashlib
import reply
import receive
import logging
import sys

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
        logger.info(f"Handle Post webdata is {webData}")
        
        # 解析XML数据
        recMsg = receive.parse_xml(webData)
        
        # 根据消息类型处理不同的消息
        if isinstance(recMsg, receive.Msg):
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            
            # 处理菜单点击事件
            if recMsg.MsgType == 'event' and recMsg.Event == 'CLICK':
                logger.info(f"recMsg.EventKey is {recMsg.EventKey}")
                if recMsg.EventKey == '2':
                    # 处理观影券领取事件
                    content = "关注公众号！"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                    
                elif recMsg.EventKey == '4':
                    # 处理图片消息事件
                    replyMsg = reply.ImageMsg(toUser, fromUser, "dZ7hibV5wsIdYdwWOhRIi1u0Z4ZmJJ_fX1BLO8ewDHhOJs2FBj37YYTb0cti81GK")
                    return replyMsg.send()
                    
                elif recMsg.EventKey == '8':
                    # 处理抽奖事件
                    content = "暂时没有抽奖~"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
            
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