# encoding: utf-8

import markdown
import datetime

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.encoding import smart_unicode

markdown.HTML_REMOVED_TEXT = ""
register = template.Library()

@register.filter
def markup(text, safe='unsafe'):
    if safe == 'safe':
        safe_mode = False
    else:
        safe_mode = True
    text = markdown.markdown(text, safe_mode=safe_mode)

    text = mark_safe(text)
    return text


@register.inclusion_tag('block_article_authors.html')
def article_authors(article):
    return {'article':article}


MONTHS = {
    1: u'января',
    2: u'февраля',
    3: u'марта',
    4: u'апреля',
    5: u'мая',
    6: u'июня',
    7: u'июля',
    8: u'августа',
    9: u'сентября',
    10: u'октября',
    11: u'ноября',
    12: u'декабря',
    }


@register.filter
def human_date(date, mode=""):
    """
    Дата в привычном русскоязычном виде типа "15 августа". Если
    год отличен от текущего, он добавляется.
    mode - режимы вывода в строку через пробел
        no_year - не вводить год в любом случае
        short_month - месяц тремя буквами
    """
    if date is None:
        return u''
    try:
        current_year = datetime.date.today().year
        if current_year == date.year or 'no_year' in mode:
            format = u'%(day)s %(month)s'
        else:
            format = u'%(day)s %(month)s %(year)s'

        month = MONTHS[date.month]
        if 'short_month' in mode:
            month = month[:3]

        return format % dict(day = date.day,
            month = month,
            year = date.year)
    except AttributeError:
        if not settings.DEBUG:
            return smart_unicode(date)
        raise


@register.filter
def human_month(monthNumber):
    months = (u'январь', u'февраль', u'март', u'апрель', u'май', u'июнь', u'июль', u'август',
              u'сентябрь', u'октябрь', u'ноябрь', u'декабрь')
    return months[monthNumber - 1]
