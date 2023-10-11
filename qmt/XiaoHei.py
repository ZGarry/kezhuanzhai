from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=98d541da10f2e9421e040869d50acaa5c924b5c4d9dc131da9b662bb5231a7bc'
secret = 'SEC7ec33ba12c5614773cfd949363693a0594185b040617b9c05c04813a2feb9265'
xiaohei = DingtalkChatbot(webhook, secret=secret)
xiaohei.send_text("小黑正常为您服务中...")