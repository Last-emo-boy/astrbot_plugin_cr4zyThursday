# main.py
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType
import urllib.request

@register("crazythursday", "Your Name", "一个疯狂星期四插件(纯标准库)", "1.0.0", "repo url")
class CrazyThursdayPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        如果消息中包含“疯狂星期四”，则访问指定接口并返回内容
        """
        text = event.get_plain_text()  # 获取消息的纯文本
        if "疯狂星期四" in text:
            try:
                # 使用标准库 urllib 完成HTTP请求
                with urllib.request.urlopen("https://kfc-crazy-thursday.vercel.app/api/index") as resp:
                    result_bytes = resp.read()
                    result_text = result_bytes.decode("utf-8", errors="replace")
            except Exception as e:
                # 处理网络异常
                result_text = f"获取信息失败: {e}"

            # 将接口返回结果发送回用户
            yield event.plain_result(result_text)
