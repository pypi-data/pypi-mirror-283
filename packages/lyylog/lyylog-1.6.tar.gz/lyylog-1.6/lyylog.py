import sys
import inspect
import logging
from datetime import datetime
import os
from functools import partial
from colorlog import ColoredFormatter

# 全局日志处理器和 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置为最低级别，以便捕获所有级别的日志

# 日志目录名称
subdir_name = "lyylog"
first_logging = True

# 获取当前工作目录
current_working_dir = os.getcwd()
print("in lyylog, getcwd="+current_working_dir)
# 获取不带扩展名的文件名
log_filename_prefix = "logfile"

# 确保日志目录存在
log_dir_path = os.path.join(current_working_dir, subdir_name)
if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# 创建不同级别的日志文件处理器
file_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

info_filename = f"{log_filename_prefix}_info_{datetime.now().strftime('%Y-%m-%d')}.log"
warning_filename = f"{log_filename_prefix}_warning_{datetime.now().strftime('%Y-%m-%d')}.log"
error_filename = f"{log_filename_prefix}_error_{datetime.now().strftime('%Y-%m-%d')}.log"
debug_filename = f"{log_filename_prefix}_debug_{datetime.now().strftime('%Y-%m-%d')}.log"

info_handler = logging.FileHandler(os.path.join(log_dir_path, info_filename), encoding='utf-8')
warning_handler = logging.FileHandler(os.path.join(log_dir_path, warning_filename), encoding='utf-8')
error_handler = logging.FileHandler(os.path.join(log_dir_path, error_filename), encoding='utf-8')
debug_handler = logging.FileHandler(os.path.join(log_dir_path, debug_filename), encoding='utf-8')

for handler in (info_handler, warning_handler, error_handler, debug_handler):
    handler.setFormatter(file_formatter)

# 为每个处理器设置级别
info_handler.setLevel(logging.INFO)
warning_handler.setLevel(logging.WARNING)
error_handler.setLevel(logging.ERROR)
debug_handler.setLevel(logging.DEBUG)

# 将处理器添加到logger
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(debug_handler)

def get_caller_info():
    frame_info = inspect.stack()[2]  # 获取上两层调用者的信息
    file_name = frame_info.filename
    line_number = frame_info.lineno
    function_name = frame_info.function
    return file_name, line_number, function_name

def log(*args, level="info", debug=False):
    # 获取调用者信息
    file_name, line_number, function_name = get_caller_info()

    # 将所有参数转换为字符串并用空格连接
    message = ' '.join(str(arg) for arg in args)

    # 格式化日志消息，包含调用者文件名、行号和函数名
    formatted_message = f"[{file_name}:{line_number}] [{function_name}] {message}"

    # 第一次写入日志前提示日志文件路径
    global first_logging
    if first_logging:
        first_logging = False
        logger.info(f"日志文件路径: {os.path.abspath(info_filename)}")

    # 记录日志到文件
    if level.lower() == "error":
        logger.error(formatted_message)
    elif level.lower() == "warning":
        logger.warning(formatted_message)
    elif level.lower() == "debug":
        logger.debug(formatted_message)
    else:
        logger.info(formatted_message)

logdebug = partial(log, level="debug")
loginfo = partial(log, level="info")
logwarn = partial(log, level="warning")
logerr = partial(log, level="error")
logerror = partial(log, level="error")


class LoguruClass:
    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }

    def __init__(self, subdir="loguru", log_level="DEBUG"):
        self.subdir = subdir
        if not os.path.exists(self.subdir):
            os.mkdir(self.subdir)
        self.setup_logger()
        self.set_log_level(log_level)

    def get_log_file_name(self, level):
        current_date = datetime.now().strftime("%Y-%m-%d")
        return f"{os.getcwd()}/{self.subdir}/loguru_{current_date}_{level}.log"

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)
        file_handler = TimedRotatingFileHandler(filename=self.get_log_file_name("info"), when="midnight", interval=1, backupCount=7, encoding='utf-8')
        file_handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter("[%(asctime)s] [Line:%(lineno)d] [%(levelname)s]  %(message)s", "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def set_log_level(self, log_level):
        self.logger.setLevel(self.LOG_LEVELS.get(log_level.upper(), logging.DEBUG))

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)


if __name__ == "__main__":
    log("Test message")
    logerror("This is an error message.")