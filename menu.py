import requests
import json
import logging

logger = logging.getLogger(__name__)

class WeChatMenu:
    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret
        self.access_token = None

    def get_access_token(self):
        """获取access_token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.appsecret}"
        try:
            response = requests.get(url)
            result = response.json()
            if 'access_token' in result:
                self.access_token = result['access_token']
                logger.info("获取access_token成功")
                return self.access_token
            else:
                logger.error(f"获取access_token失败: {result}")
                return None
        except Exception as e:
            logger.error(f"获取access_token异常: {str(e)}")
            return None

    def create_menu(self):
        """创建自定义菜单"""
        if not self.access_token:
            if not self.get_access_token():
                return False

        url = f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={self.access_token}"
        
        # 菜单配置
        menu_data = {
            "button": [
                {
                    "name": "简单分析", 
                    "sub_button": [
                        {
                            "name": "涨停分析", 
                            "type": "click", 
                            "key": "zhangtingfenxi"
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(url, json=menu_data)
            result = response.json()
            if result.get('errcode') == 0:
                logger.info("创建菜单成功")
                return True
            else:
                logger.error(f"创建菜单失败: {result}")
                return False
        except Exception as e:
            logger.error(f"创建菜单异常: {str(e)}")
            return False

    def delete_menu(self):
        """删除自定义菜单"""
        if not self.access_token:
            if not self.get_access_token():
                return False

        url = f"https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={self.access_token}"
        try:
            response = requests.get(url)
            result = response.json()
            if result.get('errcode') == 0:
                logger.info("删除菜单成功")
                return True
            else:
                logger.error(f"删除菜单失败: {result}")
                return False
        except Exception as e:
            logger.error(f"删除菜单异常: {str(e)}")
            return False 