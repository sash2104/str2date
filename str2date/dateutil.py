#!/usr/bin/env python
# coding: utf-8

""" 日付操作に関する便利関数群 """

import math

# Utility functions, adapted from Python's Demo/classes/Dates.py, which
# also assumes the current Gregorian calendar indefinitely extended in
# both directions.  Difference:  Dates.py calls January 1 of year 0 day
# number 1.  The code here calls January 1 of year 1 day number 1.  This is
# to match the definition of the "proleptic Gregorian" calendar in Dershowitz
# and Reingold's "Calendrical Calculations", where it's the base calendar
# for all computations.  See the book for algorithms for converting between
# proleptic Gregorian ordinals and many other calendar systems.

# -1 is a placeholder for indexing purposes.
DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.
dbm = 0
for dim in DAYS_IN_MONTH[1:]:
    DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
del dbm, dim

def is_leap(year):
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def doy_to_monthday(doy, year):
    " convert day-of-year to month and day "
    assert 1 <= doy <= 365 + is_leap(year)
    if doy <= 31:
        return 1, doy
    if doy <= 59 + is_leap(year):
        return 2, doy-31
    month = math.floor(doy/30) + 1
    day = doy%30 - math.floor(0.6 * (month + 1)) + 3 - is_leap(year)
    if day <= 0:
        month -= 1
        day = DAYS_IN_MONTH[month] - day
    return month, day
