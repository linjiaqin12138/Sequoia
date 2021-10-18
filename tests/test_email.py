import unittest

import settings
from notification import mail
import logging


def test_email():
    settings.init()
    mail("测试1")
    mail("测试2")


logging.basicConfig(format='%(asctime)s %(message)s', filename='../sequoia.log')
logging.getLogger().setLevel(logging.INFO)

test_email()
