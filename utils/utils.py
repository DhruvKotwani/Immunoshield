import logging
import os.path
import logging.handlers
import sys


def setup_logging(filepath=None, use_stdout=True, log_level=logging.INFO):

    def add_handler(loggers, handler):
        for logger in loggers:
            logger.addHandler(handler)

    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(threadName)s %(filename)s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    loggers = [logging.getLogger(''), logging.getLogger('tornado.access'), logging.getLogger('tornado.application'),
               logging.getLogger('tornado.general')]

    if filepath:
        directory = os.path.dirname(os.path.abspath(filepath))
        if not os.path.exists(directory):
            os.makedirs(directory)
        handler = logging.handlers.RotatingFileHandler(filepath, maxBytes=500 * 1024, backupCount=5)
        handler.setFormatter(formatter)
        add_handler(loggers, handler)

    if use_stdout:
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        add_handler(loggers, screen_handler)

    for logger in loggers:
        logger.setLevel(log_level)
