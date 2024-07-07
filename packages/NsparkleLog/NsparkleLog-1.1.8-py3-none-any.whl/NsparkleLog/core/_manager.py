from NsparkleLog.core._logger import Logger
from NsparkleLog.utils._types import Level
from NsparkleLog.core._level import Levels
from NsparkleLog.core._handler import NullHandler, Formatter, Handler
from NsparkleLog._env import allowed_lock_type
from NsparkleLog.utils._get_lock import get_current_lock
from typing import Dict, List

class LogManager:
    loggers: Dict[str, Logger] = {}
    colorMode: bool = True
    lock = get_current_lock()
    handlers: List[Handler] = [NullHandler()]
    level: Level = Levels.ON  # type: ignore

    @classmethod
    def _create_logger(cls, name: str, level: Level) -> Logger:
        logger = Logger(name, level)  # type: ignore
        for handler in cls.handlers:
            logger.addHandler(handler)
        cls.loggers[name] = logger
        return logger
    
    @classmethod
    def config(cls,
               handlers: List[Handler] = None, # type: ignore
               level: Level = Levels.ON,  # type: ignore
               colorMode: bool = True):
        if handlers is None:
            handlers = [NullHandler()]

        cls.handlers = handlers
        cls.level = level
        cls.colorMode = colorMode

    @classmethod
    def getLogger(cls, name: str) -> Logger:  # type: ignore
        if isinstance(cls.lock, allowed_lock_type):
            with cls.lock:  # type: ignore
                logger = cls.loggers.get(name)
                if logger is None:
                    return cls._create_logger(name, cls.level)  # type: ignore
                return logger
