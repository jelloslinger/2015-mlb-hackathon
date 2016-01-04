# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal, ROUND_HALF_UP
import logging
import time
import xlrd

from datapro.framework.util import to_utc

logger = logging.getLogger(__name__)


class Validator(object):

    def __init__(self, level='warn'):
        self._level = level
        self._message_template = None
        self.properties = None
        self.valid = None

        self.reset()

    def _check_null(self, key, value, blank_is_null, nulls_ok, level, message_template):
        if value is None:
            if nulls_ok:
                self.properties[key] = value
            else:
                self._fail(key, level, 'Nulls are not allowed', message_template)
            return False
        elif isinstance(value, str) and value == '':
            if blank_is_null:
                if nulls_ok:
                    self.properties[key] = None
                else:
                    self._fail(key, level, 'Blank strings are not allowed', message_template)
                return False
        return True


    def _fail(self, key, level, message, message_template):
        self.valid = False
        if not level:
            level = self._level
        if not message_template:
            message_template = self._message_template

        # print(key)
        # print(message_template)
        # # print(message_template.format(**{'key': key, 'message': message})
        # exit()

        # getattr(logger, level)(message_template.format(**{'key': key, 'message': message}))
        getattr(logger, level)(message_template.format(key=key, message=message))

    def reset(self, mesage_template=None):
        if mesage_template:
            self._message_template = mesage_template
        self.properties = {}
        self.valid = True

    def date(self, key, value, format, nulls_ok=False, level=None, message_template=None):
        if self._check_null(key, value, True, nulls_ok, level, message_template):
            if isinstance(format, str):
                try:
                    self.properties[key] = datetime.date(*(time.strptime(value, format)[:3]))
                except:
                    self._fail(key, level, '"{0}" could not be converted to a date'.format(value), message_template)
            else:
                try:
                    self.properties[key] = datetime.date(*(xlrd.xldate_as_tuple(value, format)[:3]))
                except:
                    self._fail(key, level, '"{0}" could not be converted to a date'.format(value), message_template)

    def datetime(self, key, value, format, tz=None, nulls_ok=False, level=None, message_template=None):
        if self._check_null(key, value, True, nulls_ok, level, message_template):
            if isinstance(format, str):
                try:
                    dt = datetime.datetime(*(time.strptime(value, format)[:6]))
                except:
                    self._fail(key, level, '"{0}" could not be converted to a date and time'.format(value), message_template)
                    return
            else:
                try:
                    dt = datetime.datetime(*(xlrd.xldate_as_tuple(value, format)[:6]))
                except:
                    self._fail(key, level, '"{0}" could not be converted to a date and time'.format(value), message_template)
                    return

            if tz is not None:
                dt = to_utc(dt, tz)
            self.properties[key] = dt

    def decimal(self, key, value, precision, nulls_ok=False, level=None, message_template=None):
        if self._check_null(key, value, True, nulls_ok, level, message_template):
            qp = '1.{places}'.format(places='0'*precision)
            try:
                self.properties[key] = Decimal(value).quantize(Decimal(qp), rounding=ROUND_HALF_UP)
            except:
                self._fail(key, level, '"{0}" could not be converted to a number'.format(value), message_template)

    def int(self, key, value, nulls_ok=False, level=None, message_template=None):
        if self._check_null(key, value, True, nulls_ok, level, message_template):
            try:
                self.properties[key] = int(value)
            except:
                self._fail(key, level, '"{0}" could not be converted to an integer'.format(value), message_template)

    def string(self, key, value, blanks_ok=False, convert_nulls_to_blank=False, max_length=0, nulls_ok=False, level=None, message_template=None):

        if value is None:
            if convert_nulls_to_blank:
                if blanks_ok:
                    self.properties[key] = ''
                else:
                    self._fail(key, level, 'Interpreted null as blank, but blank strings are not allowed', message_template)
            elif not nulls_ok:
                self._fail(key, level, 'Nulls are not allowed', message_template)
        elif value == '' and not blanks_ok:
            self._fail(key, level, 'Blank strings are not allowed', message_template)
        else:
            if 0 < max_length < len(value):
                self._fail(
                    key,
                    level,
                    '"{0}" is {1} characters long, but the maximum allowed length is {2}'.format(
                        value,
                        len(value),
                        max_length
                    ),
                    message_template
                )
            else:
                self.properties[key] = value
