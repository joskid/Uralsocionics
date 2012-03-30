# encoding: utf-8

import markdown

from django import template
from django.utils.safestring import mark_safe
from pytils.dt import MONTH_NAMES

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
    return {'article': article}


@register.filter
def human_month(monthNumber):
    return MONTH_NAMES[monthNumber - 1][1]
