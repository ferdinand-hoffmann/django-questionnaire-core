# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from questionnaire_core.models import Questionnaire

from .base import TestCaseBase


# Create your tests here.
class ModelTestCase(TestCaseBase):

    def test_questionnaire_test1_created(self):
        """Test1 questionnaire was created (from fixture)"""
        test1 = Questionnaire.objects.get(title='test1')

        self.assertEqual(test1.questions.count(), 12)
