import logging
import os
from logging.handlers import TimedRotatingFileHandler


LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)
DEFAULT_LOGFILE = os.path.join(LOG_DIR, "chaoxing.log")

FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)


def _create_stream_handler(level):
    sh = logging.StreamHandler()
    sh.setLevel(level)
    sh.setFormatter(FORMATTER)
    return sh


def _create_file_handler(logfile, level):
    # 半夜轮转日志文件，保留7天
    fh = TimedRotatingFileHandler(
        logfile, when="midnight", backupCount=7, encoding="utf-8"
    )
    fh.setLevel(level)
    fh.setFormatter(FORMATTER)
    return fh


def get_logger(name=None, level=logging.INFO, logfile=None):
    """
    Return a configured logger.
    - name: logger name (module name recommended). If None, uses root package name.
    - level: logging level (default INFO).
    - logfile: path to file. If None, uses DEFAULT_LOGFILE.
    """
    if name is None:
        # 默认使用根包名, 如果无法获取则使用"chaoxingRead"
        name = __package__ or "chaoxingRead"

    logger = logging.getLogger(name)
    if logger.handlers:
        # already configured
        logger.setLevel(level)
        return logger

    logfile = logfile or DEFAULT_LOGFILE

    logger.setLevel(level)
    logger.propagate = False

    logger.addHandler(_create_stream_handler(level))
    logger.addHandler(_create_file_handler(logfile, level))

    return logger


if __name__ == "__main__":
    # 测试日志记录器
    log = get_logger("testLogger", level=logging.DEBUG)
    log.debug("这是一条调试信息")
    log.info("这是一条信息")
    log.warning("这是一条警告信息")
    log.error("这是一条错误信息")
    log.critical("这是一条严重错误信息")
