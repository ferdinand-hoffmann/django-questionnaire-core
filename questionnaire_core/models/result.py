# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from ordered_model.models import OrderedModel

from ..fields import DynamicStorageFileField
from .questionnaire import Question, Questionnaire


class QuestionnaireResultManager(models.Manager):
    def with_answers(self):
        return self.get_queryset().prefetch_related('answers')


@python_2_unicode_compatible
class QuestionnaireResult(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    result_meta = JSONField(
        default=dict,
        help_text='Optional JSON field for application specific meta data',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionnaireResultManager()

    def initial_form_data(self):
        initial_data = OrderedDict()

        initial_data['result_set'] = self.pk
        for question in self.questionnaire.questions.all():
            form_field_id = 'q{}'.format(question.pk)
            form_field_value = question.question_type_obj.initial_field_value(self)
            if form_field_value is not None:
                initial_data[form_field_id] = form_field_value

        return initial_data

    def __str__(self):
        return u'{} ({})'.format(self.questionnaire, self.created_at)


@python_2_unicode_compatible
class QuestionAnswer(OrderedModel):
    result_set = models.ForeignKey(QuestionnaireResult, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_data = JSONField(null=True, db_index=True)

    order_with_respect_to = 'result_set'

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return '{}: {}'.format(self.question, self.answer_data)


class AnswerFile(OrderedModel):
    answer = models.OneToOneField(QuestionAnswer, related_name='file_upload', on_delete=models.CASCADE)
    file = DynamicStorageFileField()

    order_with_respect_to = 'answer'

    class Meta(OrderedModel.Meta):
        pass