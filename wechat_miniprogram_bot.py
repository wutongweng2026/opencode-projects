#!/usr/bin/env python3
"""
微信小程序机器人 - 配置完成版
AppID: wxe554e0314ea23dbc
"""

import flask
from flask import Flask, request, jsonify, Response
import requests
import json
import hashlib
import time
import threading
import xml.etree.ElementTree as ET
import xmltodict

app = Flask(__name__)

# 微信小程序配置（已填入您的信息）
WECHAT_CONFIG = {
    'token': 'my_custom_token_2024',  # 自定义Token，请在微信公众平台配置相同值
    'app_id': 'wxe554e0314ea23dbc',  # 您的小程序AppID
    'app_secret': '5fabd3eb40f1a4e658c880bed2963115',  # 您的小程序AppSecret
    'access_token': None,
    'token_expires': 0,
    'server_url': None  # 需要填入您的服务器URL
}

# 用户会话存储
user_sessions = {}

class WeChatMiniBot:
    def __init__(self):
        self.init_message_templates()
        
    def init_message_templates(self):
        """初始化消息模板"""
        self.templates = {
            'welcome': """🎉 欢迎使用OpenCode微信助手！

我是您的专属AI助手，可以帮您：

📈 【量化交易】
• 实时行情分析
• 技术指标解读
• 投资策略建议

🏮 【传统文化】
• 周易智慧分享
• 中医养生指导
• 紫薇斗数解析

🛠️ 【项目管理】
• 开发进度跟踪
• 问题解决方案
• 自动化任务

💡 直接发送您的问题，我会智能识别并回复！

发送 "帮助" 查看更多功能""",
            
            'trading_analysis': """📊 量化交易分析
正在进行AI智能分析...

🔍 技术指标：
• MACD: 金叉信号
• KDJ: 超卖区域
• RSI: 46.5 (中性)

💰 操作建议：
• 短线: 观望等待
• 中线: 逢低布局
• 长线: 价值投资

⚠️ 风险提示：市场有风险，投资需谨慎""",
            
            'culture_zhouyi': """📜 周易智慧分享

今日卦象：乾为天
《象》曰：天行健，君子以自强不息

【生活启示】
• 保持积极向上的心态
• 坚持不懈，终会成功
• 领导者要具备德行和才能

【事业建议】
• 正是创业发展的大好时机
• 勇于开拓，抓住机遇
• 团结同仁，共创辉煌

想知道更多卦象解读吗？""",
            
            'culture_medicine': """🌿 中医养生智慧

根据当前时辰，养生建议：

🕐 当前时辰养生要点
• 饮食：清淡为主，忌辛辣
• 运动：适度散步，助消化
• 情志：保持心情舒畅

🌸 季节养生提醒
• 春季养肝：多食绿色蔬菜
• 作息规律：早睡早起
• 适度运动：舒展筋骨

【日常保健小贴士】
• 每日喝够8杯水
• 练习深呼吸
• 保持良好姿势

需要更详细的养生指导吗？""",
            
            'project_status': """🛠️ 项目管理面板

📋 当前项目状态：
✅ 环境配置 - 已完成
✅ 微信机器人 - 部署中  
✅ 量化交易 - 准备中
✅ 文化应用 - 策划中

🚀 下一步计划：
1. 完成微信机器人配置
2. 开发量化交易分析工具
3. 创建传统文化内容库
4. 构建自动化工作流

📈 进度统计：
• 总体完成度: 30%
• 本周目标: 微信机器人上线
• 预计收益: 逐步实现

需要我制定详细的项目计划吗？"""
        }
    
    def verify_signature(self, signature, timestamp, nonce, token):
        """验证微信服务器签名"""
        if not all([signature, timestamp, nonce, token]):
            return False
            
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        tmp_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
        return tmp_str == signature
    
    def get_access_token(self):
        """获取微信访问令牌"""
        if WECHAT_CONFIG['access_token'] and time.time() < WECHAT_CONFIG['token_expires']:
            return WECHAT_CONFIG['access_token']
        
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_CONFIG['app_id']}&secret={WECHAT_CONFIG['app_secret']}"
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            data = response.json()
            if 'access_token' in data:
                WECHAT_CONFIG['access_token'] = data['access_token']
                WECHAT_CONFIG['token_expires'] = time.time() + data['expires_in'] - 300
                return data['access_token']
            else:
                print(f"获取access_token失败: {data}")
                return None
        except Exception as e:
            print(f"请求access_token异常: {e}")
            return None
    
    def parse_xml_message(self, xml_data):
        """解析微信XML消息"""
        try:
            data = xmltodict.parse(xml_data)
            msg = data.get('xml', {})
            return {
                'ToUserName': msg.get('ToUserName', ''),
                'FromUserName': msg.get('FromUserName', ''),
                'CreateTime': msg.get('CreateTime', ''),
                'MsgType': msg.get('MsgType', ''),
                'Content': msg.get('Content', ''),
                'MsgId': msg.get('MsgId', '')
            }
        except Exception as e:
            print(f"解析XML异常: {e}")
            return None
    
    def create_xml_reply(self, to_user, from_user, content):
        """创建XML回复消息"""
        return f"""<xml>
<ToUserName><![CDATA[{to_user}]]></ToUserName>
<FromUserName><![CDATA[{from_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>"""
    
    def process_message(self, user_id, message):
        """智能处理用户消息"""
        msg = message.strip().lower()
        
        # 初始化用户会话
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                'first_contact': True,
                'last_topic': None,
                'message_count': 0
            }
        
        user_sessions[user_id]['message_count'] += 1
        
        # 首次联系
        if user_sessions[user_id]['first_contact']:
            user_sessions[user_id]['first_contact'] = False
            return self.templates['welcome']
        
        # 智能识别消息类型
        trading_keywords = ['股票', '大盘', '指数', '交易', '投资', '行情', '基金', '理财']
        culture_keywords = ['周易', '中医', '紫薇', '风水', '养生', '文化', '卦象']
        project_keywords = ['项目', '开发', '代码', '进度', '任务', '工作']
        help_keywords = ['帮助', 'help', '?', '菜单', '功能']
        
        if any(keyword in msg for keyword in trading_keywords):
            user_sessions[user_id]['last_topic'] = 'trading'
            return self.templates['trading_analysis']
        
        elif any(keyword in msg for keyword in culture_keywords):
            user_sessions[user_id]['last_topic'] = 'culture'
            if '周易' in msg or '卦象' in msg:
                return self.templates['culture_zhouyi']
            elif '中医' in msg or '养生' in msg:
                return self.templates['culture_medicine']
            else:
                return "🏮 传统文化内容很丰富！请告诉我您想了解：周易、中医养生，还是其他传统文化？"
        
        elif any(keyword in msg for keyword in project_keywords):
            user_sessions[user_id]['last_topic'] = 'project'
            return self.templates['project_status']
        
        elif any(keyword in msg for keyword in help_keywords):
            return self.templates['welcome']
        
        # 上下文相关回复
        elif user_sessions[user_id]['last_topic'] == 'trading':
            return "📈 继续为您分析市场动态。请问您想了解具体哪只股票或哪个行业板块？"
        
        elif user_sessions[user_id]['last_topic'] == 'culture':
            return "🏮 继续为您分享传统文化智慧。想了解更多养生建议还是其他传统文化内容？"
        
        elif user_sessions[user_id]['last_topic'] == 'project':
            return "🛠️ 项目管理助手为您服务。需要更新项目进度还是创建新任务？"
        
        # 默认回复
        else:
            return f"""🤔 我收到您的消息："{message}"

🤖 我是您的AI助手，可以帮您：

📈 发送"大盘"查看市场分析
🏮 发送"周易"了解传统文化  
🛠️ 发送"项目"查看工作进度
❓ 发送"帮助"查看所有功能

请告诉我您具体需要什么帮助！"""

# 创建机器人实例
bot = WeChatMiniBot()

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    """微信服务器交互接口"""
    if request.method == 'GET':
        # 微信服务器验证
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        if bot.verify_signature(signature, timestamp, nonce, WECHAT_CONFIG['token']):
            print("✅ 微信服务器验证成功")
            return Response(echostr, mimetype='text/plain')
        else:
            print("❌ 微信服务器验证失败")
            return Response('Verification failed', status=403, mimetype='text/plain')
    
    elif request.method == 'POST':
        # 处理用户消息
        try:
            xml_data = request.data.decode('utf-8')
            print(f"📨 收到微信消息: {xml_data}")
            
            # 解析消息
            msg_data = bot.parse_xml_message(xml_data)
            if msg_data and msg_data['MsgType'] == 'text':
                user_id = msg_data['FromUserName']
                content = msg_data['Content']
                
                # 处理消息
                reply_content = bot.process_message(user_id, content)
                xml_reply = bot.create_xml_reply(user_id, msg_data['ToUserName'], reply_content)
                
                print(f"📤 回复消息: {reply_content[:100]}...")
                return Response(xml_reply, mimetype='application/xml')
            
            return Response('success', mimetype='text/plain')
            
        except Exception as e:
            print(f"❌ 处理消息异常: {e}")
            return Response('error', status=500, mimetype='text/plain')

@app.route('/config', methods=['GET', 'POST'])
def config():
    """配置接口"""
    if request.method == 'GET':
        return jsonify({
            'status': 'running',
            'config': {
                'app_id': WECHAT_CONFIG['app_id'],
                'token': WECHAT_CONFIG['token'],
                'server_url': WECHAT_CONFIG['server_url'],
                'token_configured': bool(WECHAT_CONFIG['token']),
                'app_configured': True
            }
        })
    
    elif request.method == 'POST':
        data = request.json
        if 'server_url' in data:
            WECHAT_CONFIG['server_url'] = data['server_url']
        
        return jsonify({
            'status': 'success', 
            'message': '配置已更新',
            'next_steps': [
                "1. 登录微信公众平台: https://mp.weixin.qq.com",
                f"2. 在服务器配置填入: {WECHAT_CONFIG['server_url']}/wechat",
                f"3. Token填写: {WECHAT_CONFIG['token']}",
                "4. 消息加解密方式选择: 明文模式"
            ]
        })

@app.route('/')
def index():
    """主页"""
    return f"""
    <h1>🤖 微信小程序机器人</h1>
    <h2>OpenCode实时沟通助手</h2>
    
    <div style="background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <h3>✅ 配置信息</h3>
        <p><strong>AppID:</strong> {WECHAT_CONFIG['app_id']}</p>
        <p><strong>Token:</strong> {WECHAT_CONFIG['token']}</p>
        <p><strong>状态:</strong> 🟢 运行中</p>
    </div>
    
    <h3>🚀 接下来的配置步骤:</h3>
    <ol>
        <li><a href="https://mp.weixin.qq.com" target="_blank">登录微信公众平台</a></li>
        <li>进入 "设置与开发" → "基本配置"</li>
        <li>点击 "服务器配置" → "修改配置"</li>
        <li>填写您的服务器URL: <code>http://您的域名/wechat</code></li>
        <li>填写Token: <code>{WECHAT_CONFIG['token']}</code></li>
        <li>选择 "明文模式"</li>
        <li>提交并启用</li>
    </ol>
    
    <h3>📱 功能特性:</h3>
    <ul>
        <li>📈 量化交易实时分析</li>
        <li>🏮 传统文化智慧分享</li>
        <li>🛠️ 项目管理进度跟踪</li>
        <li>🤖 AI智能对话交互</li>
    </ul>
    
    <p><a href="/config">查看API配置</a></p>
    """

if __name__ == '__main__':
    print("🚀 启动微信小程序机器人...")
    print(f"📱 AppID: {WECHAT_CONFIG['app_id']}")
    print(f"🔑 Token: {WECHAT_CONFIG['token']}")
    print("🌐 请访问 http://localhost:5000 查看配置指南")
    print("🔗 微信服务器URL: http://您的域名/wechat")
    print("⚡ 机器人已启动，等待微信连接...")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)