import unittest

import settings
from notification import push
from notification import strategy
from notification import statistics
import logging


def test_push():
    settings.init()
    push("测试")


def test_strategy():
    settings.init()
    strategy("")
    strategy("1")


logging.basicConfig(format='%(asctime)s %(message)s', filename='../sequoia.log')
logging.getLogger().setLevel(logging.INFO)
