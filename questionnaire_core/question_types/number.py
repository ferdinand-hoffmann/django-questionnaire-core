# -*- coding: utf-8 -*-
from decimal import Decimal

from django import forms

from .base import QuestionTypeBase


class NumberBase(QuestionTypeBase):
    class Meta:
        abstract = True

    def clean_question_options(self, question_options):
        """
        expected question_options format:
        {
            min: 1,
            max: 10
        }
        """

        if 'min' in question_options:
            try:
                question_options['min'] = int(question_options['min'])
            except ValueError:
                raise forms.ValidationError('value for "min" is not an integer')

        if 'max' in question_options:
            try:
                question_options['max'] = int(question_options['max'])
            except ValueError:
                raise forms.ValidationError('value for "max" is not an integer')

        return question_options


class NumberInteger(NumberBase):
    class Meta:
        name = 'number_integer'
        verbose_name = 'Number (Integer)'
        widget_class = forms.NumberInput

    def formfield(self, result_set):
        min_value = self.question.question_options.get('min')
        max_value = self.question.question_options.get('max')

        return forms.IntegerField(
            widget=self.formfield_widget(),
            label=self.question.question_text,
            required=self.question.required,
            min_value=min_value,
            max_value=max_value,
        )


class NumberDecimal(NumberBase):
    class Meta:
        name = 'number_decimal'
        verbose_name = 'Number (Decimal)'
        widget_class = forms.NumberInput

    def clean_question_options(self, question_options):
        """
        expected question_options format:
        {
            min: 1,
            max: 10,
            decimal_places: 2
        }
        """

        question_options = super(NumberDecimal, self).clean_question_options(question_options)

        if 'decimal_places' in question_options:
            try:
                question_options['decimal_places'] = int(question_options['decimal_places'])
            except ValueError:
                raise forms.ValidationError('value for "decimal_places" is not an integer')

        return question_options

    def clean_answer_data(self, data):
        if data is not None:
            return str(data.quantize(Decimal('.00')))

    def formfield(self, result_set):
        min_value = self.question.question_options.get('min')
        max_value = self.question.question_options.get('max')
        decimal_places = self.question.question_options.get('decimal_places', 2)

        return forms.DecimalField(
            widget=self.formfield_widget(),
            label=self.question.question_text,
            required=self.question.required,
            min_value=min_value,
            max_value=max_value,
            decimal_places=decimal_places,
        )


class NumberPercent(NumberBase):
    class Meta:
        name = 'number_percent'
        verbose_name = 'Number (Percent)'
        widget_class = forms.NumberInput

    def formfield(self, result_set):
        min_value = self.question.question_options.get('min', 0)
        max_value = self.question.question_options.get('max', 100)

        return forms.IntegerField(
            widget=self.formfield_widget(),
            label=self.question.question_text,
            required=self.question.required,
            min_value=min_value,
            max_value=max_value,
        )
