# -*- coding: utf-8 -*-

import calendar
import datetime
from math import ceil

from sqlalchemy import Column
from sqlalchemy.types import *

from datapro import IdMixin, Model


class Date(Model, IdMixin):
    __schema__ = 'common'
    __table_name__ = 'Date'
    __table_name_mask__ = '{__table_type__}_{__table_name__}'
    __table_type__ = 'DIM'

    date = Column(DATE, nullable=False, unique=True)
    full = Column(VARCHAR(255), nullable=False)
    year = Column(SMALLINT, nullable=False)
    half = Column(SMALLINT, nullable=False)
    quarter = Column(SMALLINT, nullable=False)
    month = Column(SMALLINT, nullable=False)
    dayOfYear = Column(SMALLINT, nullable=False)
    dayOfYearNoLeap = Column(SMALLINT, nullable=False)
    dayOfQuarter = Column(SMALLINT, nullable=False)
    yearOfWeekYear = Column(SMALLINT, nullable=False)
    weekOfWeekYear = Column(SMALLINT, nullable=False)
    dayOfMonth = Column(SMALLINT, nullable=False)
    dayOfWeek = Column(SMALLINT, nullable=False)
    yearAndHalf = Column(VARCHAR(255), nullable=False)
    yearAndQuarter = Column(VARCHAR(255), nullable=False)
    yearAndWeek = Column(VARCHAR(255), nullable=False)
    monthNameShort = Column(VARCHAR(255), nullable=False)
    monthNameLong = Column(VARCHAR(255), nullable=False)
    dayOfWeekNameShort = Column(VARCHAR(255), nullable=False)
    dayOfWeekNameLong = Column(VARCHAR(255), nullable=False)
    yearAndMonthNameShort = Column(VARCHAR(255), nullable=False)
    yearAndMonthNameLong = Column(VARCHAR(255), nullable=False)
    weekend = Column(VARCHAR(255), nullable=False)
    isLastDayOfMonth = Column(BOOLEAN, nullable=False)

    @classmethod
    def from_date(cls, d):
        half = int(ceil(float(d.month) / 6.0))
        quarter = int(ceil(float(d.month) / 3.0))
        dayOfYear = d.timetuple().tm_yday
        dayOfYearNoLeap = dayOfYear
        if calendar.isleap(d.year):
            if dayOfYear == 60:
                dayOfYearNoLeap = 0
            elif dayOfYear > 60:
                dayOfYearNoLeap -= 1
        dayOfQuarter = (d - datetime.date(d.year, (3 * (quarter - 1)) + 1, 1)).days + 1
        iso = d.isocalendar()
        isLastDayOfMonth = True if (d.day == calendar.monthrange(d.year, d.month)[1]) else False

        return cls(
            date=d,
            full=d.__format__('%A, %B ') + str(d.day) + d.__format__(', %Y'),
            year=d.year,
            half=half,
            quarter=quarter,
            month=d.month,
            dayOfYear=dayOfYear,
            dayOfYearNoLeap=dayOfYearNoLeap,
            dayOfQuarter=dayOfQuarter,
            yearOfWeekYear=iso[0],     # ISO calendar year
            weekOfWeekYear=iso[1],     # ISO calendar week number
            dayOfMonth=d.day,
            dayOfWeek=iso[2],          # ISO calendar day of week
            yearAndHalf='H' + str(half) + ' ' + str(d.year),
            yearAndQuarter='Q' + str(quarter) + ' ' + str(d.year),
            yearAndWeek='W' + str(iso[1]) + ' ' + str(iso[0]),
            monthNameShort=d.__format__('%b'),
            monthNameLong=d.__format__('%B'),
            dayOfWeekNameShort=d.__format__('%a'),
            dayOfWeekNameLong=d.__format__('%A'),
            yearAndMonthNameShort=d.__format__('%b %Y'),
            yearAndMonthNameLong=d.__format__('%B %Y'),
            weekend='Weekend' if iso[2] >= 6 else 'Weekday',
            isLastDayOfMonth=isLastDayOfMonth
        )


__all__ = (
    Date,
)