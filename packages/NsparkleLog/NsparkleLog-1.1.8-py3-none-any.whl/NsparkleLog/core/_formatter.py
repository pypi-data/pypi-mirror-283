from re import T
from typing import Optional
from NsparkleLog.utils._types import AnyStr, Level
from NsparkleLog.dependencies import time , re
from NsparkleLog.core._level import _levelToName
from NsparkleLog.utils._color import Color
from NsparkleLog._env import default_format , LevelColor
from NsparkleLog.core._record import LogRecord
from uuid import uuid4

class Formatter:
    """
    同时你还可以用颜色标签来标记日志的颜色
    ### 支持的格式占位符: 
     - {name}: 日志记录器名字
     - {threadName}: 线程名字
     - {threadId}: 线程ID
     - {filename}: 文件名
     - {pathname}: 文件路径
     - {lineno}: 行号
     - {funcName}: 函数名
     - {moduleName}: 模块名
     - {ProcessId}: 进程ID
     - {ProcessName}: 进程名
     - {message}: 消息
     - {level}: 日志级别
     - {localtime}: 本地时间
     - {msecs}: 本地时间毫秒
     - {utcmsecs}: UTC时间毫秒
     - {utctime}: UTC时间
     - {timestamp}: 时间戳(本地时间)
    """
    def __init__(self,
        colorMode:bool = False,
        fmt: str = default_format,
        datefmt: str = "%Y-%m-%d %H:%M:%S"
        ) -> None:
        self._fmt = fmt
        self.colorMode = colorMode
        self._date = datefmt

        # 为了让一些习惯日志字段不同颜色的患者可以配置,提供颜色字段映射
        self._logBodyColor: dict[str, Optional[str]] = {
            "timestamp": None,
            "name": None,
            "threadName": None,
            "threadId": None,
            "filename": None,
            "pathname": None,
            "lineno": None,
            "funcName": None,
            "moduleName": None,
            "ProcessId": None,
            "ProcessName": None,
            "msecs": None,
            "utcmsecs": None,
            "localtime": None,
            "utctime": None
        }

    def configuateColor(self, colorDICT: dict[str, str],raiseIfNotSupportKey: bool = False) -> None:
        """
        配置颜色映射
        ### 参数:
            - colorDICT: 颜色字典
            - raiseIfNotSupportKey: 如果key不支持,是否抛出异常
        ### 返回值:
            - None
        ### 示例:
        colors = {
           "timestamp": "bd_grey"
        }
        formatter.configuateColor(colors)
           - 这样的话,timestamp字段就会使用bd_grey颜色
        """
        for key in colorDICT.keys():
            if key in self._logBodyColor:
                self._logBodyColor[key] = colorDICT[key] # type: ignore
            elif raiseIfNotSupportKey == True:
                raise KeyError(f"key '{key}' has not suppoted")
            else: pass

    def _get_color_tag(self, field_name: str, content: str) -> str:
        if self.colorMode:
            if field_name in self._logBodyColor:
                color = self._logBodyColor[field_name]
                if not color or color not in Color.GetAvaliableColor():
                    color = "bd_white"
                return f"<{color}>{content}</{color}>"
            else:
                color = "bd_white"
                return f"<{color}>{content}</{color}>"
        return content

    def _get_levelColor_tag(self, level: Level) -> str:
        if self.colorMode:
            return f"<{LevelColor.getlevelColor(level)}>{_levelToName[level]}</{LevelColor.getlevelColor(level)}>" # type: ignore
        return _levelToName[level] # type: ignore

    def format(self, record: LogRecord) -> str:

        formatted_msg = self._fmt.format(
            timestamp=self._get_color_tag('timestamp', time.strftime(self._date, record.timestamp)),
            msecs=self._get_color_tag('msecs', str(record.msecs)),
            utcmsecs=self._get_color_tag('utcmsecs', str(record.utcmsecs)),
            localtime=self._get_color_tag('localtime', time.strftime(self._date, record.timestamp)),
            utctime=self._get_color_tag('utctime', time.strftime(self._date, record.utctime)),
            level=self._get_levelColor_tag(record.level),
            threadName=self._get_color_tag('threadName', record.threadName), # type: ignore
            threadId=self._get_color_tag('threadId', str(record.threadId)),
            filename=self._get_color_tag('filename', record.filename), # type: ignore
            pathname=self._get_color_tag('pathname', record.pathname), # type: ignore
            lineno=self._get_color_tag('lineno', str(record.lineno)),
            funcName=self._get_color_tag('funcName', record.funcName), # type: ignore
            moduleName=self._get_color_tag('moduleName', record.moduleName), # type: ignore
            ProcessId=self._get_color_tag('ProcessId', str(record.ProcessId)),
            ProcessName=self._get_color_tag('ProcessName', record.ProcessName), # type: ignore
            name=self._get_color_tag('name', record.name),
            message=record.message
        )
        if self.colorMode:
            return Color.renderByHtml(formatted_msg)
        return formatted_msg
