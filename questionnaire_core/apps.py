# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class QuestionnaireCoreConfig(AppConfig):
    name = 'questionnaire_core'

    def ready(self):
        # validate settings on startup
        from . import settings  # NOQA
