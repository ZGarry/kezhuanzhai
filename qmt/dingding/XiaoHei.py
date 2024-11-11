from dingtalkchatbot.chatbot import DingtalkChatbot
from Settings import dingding_talk_webhook, dingding_talk_secret

webhook = dingding_talk_webhook
secret = dingding_talk_secret
xiaohei = DingtalkChatbot(webhook, secret=secret)
xiaohei.send_text("小黑正常为您服务中...")
