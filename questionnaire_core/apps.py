# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class QuestionnaireCoreConfig(AppConfig):
    name = 'questionnaire_core'

    def ready(self):
        # validate settings on startup
        from . import settings  # NOQA

        print('xncksjdfnksd')
        from questionnaire_core.models import Question
        from questionnaire_core.models.questionnaire import available_question_types

        question_type_field = Question._meta.get_field('question_type')
        question_type_field.choices = list(available_question_types())
