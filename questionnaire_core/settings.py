# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage
from django.utils.module_loading import import_string


upload_storage = None
upload_to_handler = None
upload_allowed_file_extensions = tuple()

# validate & load QUESTIONNAIRE_CORE_UPLOAD_STORAGE
if getattr(settings, 'QUESTIONNAIRE_CORE_UPLOAD_STORAGE', None):
    try:
        storage_class = import_string(getattr(settings, 'QUESTIONNAIRE_CORE_UPLOAD_STORAGE'))
        upload_storage = storage_class()
        if not isinstance(upload_storage, Storage):
            raise ImproperlyConfigured(
                'User-defined QUESTIONNAIRE_CORE_UPLOAD_STORAGE is not a subclass of django.core.files.storage.Storage'
            )
    except ImportError:
        raise ImproperlyConfigured('Could not import user-defined QUESTIONNAIRE_CORE_UPLOAD_STORAGE')

# validate & load QUESTIONNAIRE_CORE_UPLOAD_TO_HANDLER
if getattr(settings, 'QUESTIONNAIRE_CORE_UPLOAD_TO_HANDLER', None):
    try:
        upload_to_handler = import_string(getattr(settings, 'QUESTIONNAIRE_CORE_UPLOAD_TO_HANDLER'))
        if not callable(upload_to_handler):
            raise ImproperlyConfigured('User-defined QUESTIONNAIRE_CORE_UPLOAD_TO_HANDLER is not callable.')
    except ImportError:
        raise ImproperlyConfigured('Could not import user-defined QUESTIONNAIRE_CORE_UPLOAD_TO_HANDLER')

# validate QUESTIONNAIRE_CORE_UPLOAD_ALLOWED_FILE_EXTENSIONS
if getattr(settings, 'QUESTIONNAIRE_CORE_UPLOAD_ALLOWED_FILE_EXTENSIONS', None):
    if not isinstance(getattr(settings, 'QUESTIONNAIRE_CORE_UPLOAD_ALLOWED_FILE_EXTENSIONS', list()), (list, tuple)):
        raise ImproperlyConfigured(
            'User-defined QUESTIONNAIRE_CORE_UPLOAD_ALLOWED_FILE_EXTENSIONS must be a list or tuple.'
        )
    else:
        upload_allowed_file_extensions = getattr(settings, 'QUESTIONNAIRE_CORE_UPLOAD_ALLOWED_FILE_EXTENSIONS')
