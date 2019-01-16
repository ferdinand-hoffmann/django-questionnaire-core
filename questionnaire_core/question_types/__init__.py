# -*- coding: utf-8 -*-
from .base import QuestionTypeRegistry  # NOQA

from .boolean import Boolean, BooleanYesNo  # NOQA
from .choices import Choices, ChoicesMultiple  # NOQA
from .file_upload import FileUpload  # NOQA
from .multiple import MultipleText  # NOQA
from .number import NumberDecimal, NumberInteger, NumberPercent  # NOQA
from .range import RangeSlider  # NOQA
from .text import TextShort, TextLong  # NOQA
