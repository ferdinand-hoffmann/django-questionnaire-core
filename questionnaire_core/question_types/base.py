# -*- coding: utf-8 -*-
import inspect

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.template.engine import Engine
from django.template.exceptions import TemplateDoesNotExist
from django.utils.six import add_metaclass


template_engine = Engine.get_default()


class QuestionTypeRegistry(object):
    """Registry for question type classes."""
    _registered_types = {}

    @classmethod
    def register(cls, question_type):
        name = question_type.meta.name
        cls._registered_types[name] = question_type

    @classmethod
    def unregister(cls, question_type):
        name = question_type.meta.name
        if name in cls._registered_types:
            del cls._registered_types[name]

    @classmethod
    def get_question_types(cls):
        return cls._registered_types

    @classmethod
    def get_question_type(cls, name):
        return cls._registered_types[name]


class Options(object):
    """Class to hold `meta` options of a question type class."""
    REQUIRED = ('name', 'verbose_name')

    def __init__(self, cls, meta):
        self.name = meta.get('name', None)
        self.verbose_name = meta.get('verbose_name', None)
        self.multiple = meta.get('multiple', False)
        self.widget_class = meta.get('widget_class', None)
        self.widget_template_name = None
        self.widget_option_template_name = None

        for required_option in self.REQUIRED:
            if not getattr(self, required_option, None):
                raise AttributeError('{}.Meta missing required field "{}"'.format(cls.__name__, required_option))

        self.cls = cls

        for template_key in ('template_name', 'option_template_name'):
            self.select_template(meta, template_key)

    def select_template(self, meta, template_key):
        """Select template for the formfield widget."""
        meta_template_key = 'widget_{}'.format(template_key)
        if meta.get(meta_template_key):
            # try to load explicitly specified template
            custom_template = template_engine.get_template(meta.get(meta_template_key))
            setattr(self, meta_template_key, custom_template.name)
        else:
            # fallback to packaged template
            try:
                if template_key == 'template_name':
                    default_template = 'questionnaire_core/widgets/{name}.html'.format(name=self.name)
                elif template_key == 'option_template_name':
                    default_template = 'questionnaire_core/widgets/{name}_option.html'.format(name=self.name)
                else:
                    return
                packaged_template = template_engine.get_template(default_template)
                setattr(self, meta_template_key, packaged_template.name)
            except TemplateDoesNotExist:
                # or use the django default template for the widget
                pass


class QuestionTypeMeta(type):
    """Meta class for question type classes.

    Responsible for registering question type classes with QuestionTypeRegistry
    and setting up the `meta` attribute of question type classes.
    """
    def __new__(mcs, name, bases, attrs):
        super_new = super(QuestionTypeMeta, mcs).__new__

        # register only subclasses of QuestionTypeBase not QuestionTypeBase itself
        if name == 'QuestionTypeBase':
            return super_new(mcs, name, bases, attrs)

        attr_meta = attrs.pop('Meta', None)

        # don't register abstract classes
        if getattr(attr_meta, 'abstract', False):
            return super_new(mcs, name, bases, attrs)

        if not attr_meta or not inspect.isclass(attr_meta):
            raise AttributeError('{}.Meta attribute missing or not a class'.format(name))

        new_class = super_new(mcs, name, bases, attrs)

        # create meta attribute (instance of QuestionTypeOptions) from new_class.Meta (similar to Model._meta)
        setattr(new_class, 'meta', Options(new_class, attr_meta.__dict__))

        QuestionTypeRegistry.register(new_class)

        return new_class


@add_metaclass(QuestionTypeMeta)
class QuestionTypeBase(object):
    """Base class for question type classes"""

    def __init__(self, question):
        self.question = question

    def clean_question_options(self, question_options):
        """Clean question options (`Question.question_options`).

        Override to implement any custom validations of the question options of the question type.

        :param question_options: django admin form field data
        :type question_options: dict
        :return: cleaned form field data
        :rtype: dict
        :raises: django.forms.ValidationError: Validation error
        """
        return question_options

    def clean_answer_data(self, data):
        """Clean answer data (`QuestionAnswer.answer_data`).

        :param data: data returned from the formfield
        :return: cleaned formfield data
        :raises: django.forms.ValidationError: Validation error
        """
        return data

    def formfield(self, result_set):
        """Form field for the question type.

        :param result_set: result set of the current form
        :type result_set: questionnaire_core.models.QuestionnaireResult
        :return: django form field for the question type
        :rtype: django.forms.Field
        """
        raise NotImplementedError

    def formfield_widget(self, **kwargs):
        """Setup and return the widget for the formfield."""
        widget_attrs = self.formfield_widget_attrs()
        if 'attrs' in kwargs:
            widget_attrs.update(kwargs.get('attrs'))
        kwargs['attrs'] = widget_attrs
        widget = self.widget_class()(**kwargs)
        # set template attribute(s) of the widget
        for template_key in ('template_name', 'option_template_name'):
            meta_template_key = 'widget_{}'.format(template_key)
            if getattr(self.question.question_type_obj.meta, meta_template_key) and hasattr(widget, template_key):
                setattr(widget, template_key, getattr(self.question.question_type_obj.meta, meta_template_key))
        return widget

    def widget_class(self):
        """Return the configured widget class for the formfield."""
        if not self.meta.widget_class:
            raise ValueError('{}.Meta.widget_class attribute is missing.'.format(self.__class__.__name__))
        return self.meta.widget_class

    def formfield_widget_attrs(self):
        """Setup and return the attributes for the formfield widget (based on question options)."""
        attrs = dict()
        if 'autocomplete' in self.question.question_options:
            attrs.update({'autocomplete': 'on' if self.question.question_options.get('autocomplete') else 'off'})
        return attrs

    def initial_field_value(self, result_set):
        """Return the initial formfield value based on the supplied result set."""
        if self.question.question_type_obj.meta.multiple:
            return list(result_set.answers.filter(question=self.question).values_list('answer_data', flat=True))
        else:
            try:
                answer = result_set.answers.get(question=self.question)
                return answer.answer_data
            except ObjectDoesNotExist:
                return None
            except MultipleObjectsReturned:
                raise ValueError('Multiple answers found for QuestionType with multiple=False')

    def save(self, result_set, answer_data):
        from ..models import QuestionAnswer

        if self.meta.multiple:
            assert isinstance(answer_data, list)
            for answer_data_part in answer_data:
                QuestionAnswer.objects.create(
                    result_set=result_set,
                    question=self.question,
                    answer_data=answer_data_part,
                )
        else:
            QuestionAnswer.objects.create(
                result_set=result_set,
                question=self.question,
                answer_data=answer_data,
            )
