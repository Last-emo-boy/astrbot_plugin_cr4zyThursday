import urllib.request
import datetime
import time
from typing import Dict
from astrbot import logger
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType

@register(
    "cr4zythursday",
    "w33d&Foolllll",
    "疯狂星期四插件",
    "1.2.0",
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

        # 从 config 中获取配置，如果没有用户配置，则使用默认值
        self.group_whitelist = self.config.get("group_whitelist", [])
        self.group_whitelist = [int(gid) for gid in self.group_whitelist]
        self.keywords = self.config.get("keywords", ["疯狂星期四"])
        self.only_thursday = self.config.get("only_thursday", False)
        self.exact_match_ignore = self.config.get("exact_match_ignore", False)
        self.cooldown = self.config.get("cooldown", 0)
        self.last_trigger_time: Dict[str, float] = {}
        logger.debug(f"已加载关键词列表: {self.keywords}")

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        当消息中包含配置的任意关键词时，获取疯狂星期四文案
        """
        # 群组白名单检查
        group_id_str = event.get_group_id()
        if group_id_str:  # 如果是群聊
            group_id = int(group_id_str)
            if self.group_whitelist and group_id not in self.group_whitelist:
                return
        # 如果是私聊，则不检查白名单

        msg_obj = event.message_obj
        text = (msg_obj.message_str or "").strip()

        # 判断消息中是否包含任意关键词，且不是唤醒对话
        if any(kw in text for kw in self.keywords) and not event.is_at_or_wake_command:
            is_exact_match = text in self.keywords
            skip_restrictions = self.exact_match_ignore and is_exact_match
            
            if not skip_restrictions:
                # 检查星期四限制
                if self.only_thursday and datetime.datetime.now().weekday() != 3:
                    return
                
                # 检查冷却时间
                session_id = msg_obj.session_id
                current_time = time.time()
                if self.cooldown > 0 and session_id in self.last_trigger_time:
                    elapsed = current_time - self.last_trigger_time[session_id]
                    if elapsed < self.cooldown:
                        logger.debug(f"疯狂星期四触发被冷却限制，剩余冷却时间：{self.cooldown - elapsed:.1f}秒")
                        return

            try:
                # with urllib.request.urlopen("https://vme.im/api?format=text") as resp:  
                with urllib.request.urlopen("https://vme.im/api/random?format=text") as resp:
                    result_bytes = resp.read()
                    result_text = result_bytes.decode("utf-8", errors="replace")
                
                # 更新最后触发时间
                self.last_trigger_time[msg_obj.session_id] = time.time()
            except Exception as e:
                result_text = f"获取信息失败: {e}"

            yield event.plain_result(result_text)
