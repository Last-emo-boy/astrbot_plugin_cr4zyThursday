import logging
import urllib.request
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType

logger = logging.getLogger(__name__)

@register(
    "cr4zythursday",
    "w33d",
    "一个疯狂星期四插件",
    "1.1.0",
    "https://github.com/Last-emo-boy/astrbot_plugin_cr4zyThursday"
)
class CrazyThursdayPlugin(Star):
    def __init__(self, context: Context, config: dict):
        """
        读取后台管理面板中用户配置的关键词数组(默认 ["疯狂星期四"])。
        只要消息包含任意一个关键词，都将触发访问 vme.im 并返回文本。
        """
        super().__init__(context)
        self.config = config

        # 从 config 中获取 keywords 数组，如果没有用户配置，则使用默认值
        self.keywords = self.config.get("keywords", ["疯狂星期四"])
        logger.debug(f"已加载关键词列表: {self.keywords}")

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        当消息中包含配置的任意关键词时，访问 https://vme.im/api?format=text 并返回响应。
        """
        msg_obj = event.message_obj
        text = msg_obj.message_str or ""

        # DEBUG 日志，只有在日志等级为 DEBUG 时才会输出
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

        # 判断消息中是否包含任意关键词
        if any(kw in text for kw in self.keywords):
            try:
                # with urllib.request.urlopen("https://vme.im/api?format=text") as resp:  
                with urllib.request.urlopen("https://vme.im/api/random?format=text") as resp:
                    result_bytes = resp.read()
                    result_text = result_bytes.decode("utf-8", errors="replace")
            except Exception as e:
                result_text = f"获取信息失败: {e}"

            yield event.plain_result(result_text)
