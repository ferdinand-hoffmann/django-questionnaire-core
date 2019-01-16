# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from questionnaire_core.models import Questionnaire, QuestionnaireResult

from .base import TestCaseBase


# Create your tests here.
class ModelTestCase(TestCaseBase):

    def test_form_class_gets_created(self):
        """Form class get's created for questionnaire"""
        q1 = Questionnaire.objects.get(title='test1')
        form_class = q1.build_form_class(QuestionnaireResult())
        self.assertEqual(form_class.__name__, 'QuestionnaireForm')
