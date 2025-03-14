# -*- coding: utf-8 -*-
import time

class Msg(object):
    def __init__(self):
        pass

    def send(self):
        return "success"

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        return XmlForm.format(**self.__dict)

class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{MediaId}]]></MediaId>
                </Image>
            </xml>
            """
        return XmlForm.format(**self.__dict)

class VoiceMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[voice]]></MsgType>
                <Voice>
                <MediaId><![CDATA[{MediaId}]]></MediaId>
                </Voice>
            </xml>
            """
        return XmlForm.format(**self.__dict)

class VideoMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId, title=None, description=None):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId
        self.__dict['Title'] = title if title is not None else ''
        self.__dict['Description'] = description if description is not None else ''

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[video]]></MsgType>
                <Video>
                <MediaId><![CDATA[{MediaId}]]></MediaId>
                <Title><![CDATA[{Title}]]></Title>
                <Description><![CDATA[{Description}]]></Description>
                </Video>
            </xml>
            """
        return XmlForm.format(**self.__dict)

class MusicMsg(Msg):
    def __init__(self, toUserName, fromUserName, title, description, musicUrl, hqMusicUrl=None, thumbMediaId=None):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Title'] = title
        self.__dict['Description'] = description
        self.__dict['MusicUrl'] = musicUrl
        self.__dict['HQMusicUrl'] = hqMusicUrl if hqMusicUrl is not None else musicUrl
        self.__dict['ThumbMediaId'] = thumbMediaId if thumbMediaId is not None else ''

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music>
                <Title><![CDATA[{Title}]]></Title>
                <Description><![CDATA[{Description}]]></Description>
                <MusicUrl><![CDATA[{MusicUrl}]]></MusicUrl>
                <HQMusicUrl><![CDATA[{HQMusicUrl}]]></HQMusicUrl>
                <ThumbMediaId><![CDATA[{ThumbMediaId}]]></ThumbMediaId>
                </Music>
            </xml>
            """
        return XmlForm.format(**self.__dict)

class NewsMsg(Msg):
    def __init__(self, toUserName, fromUserName, articles):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['ArticleCount'] = len(articles)
        self.__dict['Articles'] = articles

    def send(self):
        articles_xml = ""
        for article in self.__dict['Articles']:
            articles_xml += """
                <item>
                <Title><![CDATA[{Title}]]></Title>
                <Description><![CDATA[{Description}]]></Description>
                <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
                <Url><![CDATA[{Url}]]></Url>
                </item>
                """.format(**article)

        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>{ArticleCount}</ArticleCount>
                <Articles>{Articles}</Articles>
            </xml>
            """.format(
                ToUserName=self.__dict['ToUserName'],
                FromUserName=self.__dict['FromUserName'],
                CreateTime=self.__dict['CreateTime'],
                ArticleCount=self.__dict['ArticleCount'],
                Articles=articles_xml
            )
        return XmlForm 