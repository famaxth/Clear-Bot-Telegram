# -*- coding: utf-8 -*-


import logging
import datetime
import config
import os


def check_filename(filename, times=0):
    filename_ = f'{filename}_{times}.log'

    if filename_ in os.listdir(config._log_dir):
        try:
            with open(filename_, 'r') as f:
                if f.read() == '':
                    os.remove(filename_)
                    return filename_

        except:
            pass

        return check_filename(filename, times+1)

    else:
        return f'{config._log_dir}/{filename_}'


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        my_context = kwargs.pop(config._log_prefix, self.extra[config._log_prefix])

        return '[%s] %s' % (my_context, msg), kwargs


def get_file_handler():
    date = datetime.datetime.now()
    filename = f'{date.day}.{date.month}.{date.year}'
    filename = check_filename(filename)

    file_handler = logging.FileHandler(filename, encoding='utf-8')
    file_handler.setLevel(config._log_level_file)
    file_handler.setFormatter(logging.Formatter(config._log_format))

    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(config._log_level)
    stream_handler.setFormatter(logging.Formatter(config._log_format))

    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(config._log_level)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())

    logger = CustomAdapter(logger, {config._log_prefix: None})

    return logger


if config._log_dir not in os.listdir():
    os.mkdir(config._log_dir)