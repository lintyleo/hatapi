__version__ = "2.0.1"
__author__ = "ArtLinty"

# MIT License
#
# Copyright (c) 2019 立师兄Linty
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import sys


class Logger(object):
    """
    Logger Class
    """
    _logger = None
    _file_name = None
    _format = None
    FORMAT_STRING = "[%(asctime)s]-[%(levelname)s]:%(message)s"

    def __init__(self, log_path, call_path):
        """
        构造方法
        :param log_path:
        :param call_path:
        """
        # log_path：日志存放路径
        # 文件命名

        self._file_name = log_path
        self._logger = logging.getLogger(call_path)
        self._logger.setLevel(logging.DEBUG)
        self._format = logging.Formatter(self.FORMAT_STRING)

    def info(self, message):
        """
        添加信息日志
        :param message:
        :return:
        """
        fh, sh = self._console()
        self._logger.info(msg=message)
        self._remove_handler(fh, sh)

    def _remove_handler(self, fh, sh):
        self._logger.removeHandler(fh)
        self._logger.removeHandler(sh)

    def warning(self, message):
        """
        添加警告日志
        :param message:
        :return:
        """
        fh, sh = self._console()
        self._logger.warning(msg=message)
        self._remove_handler(fh, sh)

    def error(self, message):
        """
        添加错误日志
        :param message:
        :return:
        """
        fh, sh = self._console()
        self._logger.error(msg=message)
        self._remove_handler(fh, sh)

    def _console(self):
        """
        添加 Handler 到 Logger
        :return:
        """
        fh = self._get_file_handler()
        self._logger.addHandler(fh)

        sh = self._get_stream_handler()
        self._logger.addHandler(sh)

        return fh, sh

    def _get_stream_handler(self):
        """
        获取 Stream Handler
        :param formatter:
        :return:
        """
        # 创建一个SteamHandler,用于输出到控制台
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(self._format)
        return sh

    def _get_file_handler(self, ):
        """
        获取 文件 Handler
        :param formatter:
        :return:
        """
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self._file_name, encoding="utf8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self._format)
        return fh
