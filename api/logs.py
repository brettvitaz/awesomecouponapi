import logging
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter(fmt='[{asctime}] "{method} {url}" {message}', datefmt='%d/%b/%Y:%H:%M:%S %z', style='{')
file_handler = TimedRotatingFileHandler('error.log', when='d', interval=1, backupCount=5)
file_handler.setFormatter(formatter)
