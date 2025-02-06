import logging
import urllib.request
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType

# 获取当前模块 logger
logger = logging.getLogger(__name__)

@register("cr4zythursday", "w33d", "一个疯狂星期四插件", "1.0", "https://github.com/Last-emo-boy/astrbot_plugin_cr4zyThursday")
class CrazyThursdayPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        当消息中包含“疯狂星期四”时访问接口并返回响应。
        """
        msg_obj = event.message_obj

        text = msg_obj.message_str or ""

        logger.debug("=== Debug: AstrBotMessage ===")
        logger.debug("Bot ID: %s", msg_obj.self_id)
        logger.debug("Session ID: %s", msg_obj.session_id)
        logger.debug("Message ID: %s", msg_obj.message_id)
        logger.debug("Sender: %s", msg_obj.sender)
        logger.debug("Group ID: %s", msg_obj.group_id)
        logger.debug("Message Chain: %s", msg_obj.message)
        logger.debug("Raw Message: %s", msg_obj.raw_message)
        logger.debug("Timestamp: %s", msg_obj.timestamp)
        logger.debug("============================")

        if "疯狂星期四" in text:
            try:
                with urllib.request.urlopen("https://vme.im/api?format=text") as resp:
                    result_bytes = resp.read()
                    result_text = result_bytes.decode("utf-8", errors="replace")
            except Exception as e:
                result_text = f"获取信息失败: {e}"

            yield event.plain_result(result_text)
