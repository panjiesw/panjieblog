# -*- coding: utf-8 -*-
__author__ = 'panjiesw'

from datetime import datetime
from babel.dates import format_datetime

def dtm(value, fmt='full'):
	if fmt == 'full':
		fmt = "EEEE, MMMM dd, yyyy hh:mm a"
	elif fmt == 'year':
		fmt = "yyyy"
	elif fmt == 'month':
		fmt = "MMMM"
	return format_datetime(value,fmt)
