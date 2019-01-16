# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase


# Create your tests here.
class TestCaseBase(TestCase):
    fixtures = ('test1.json',)
