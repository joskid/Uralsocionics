# -*- coding: utf-8 -*-
from django.template import Context, loader
from django.core.mail import EmailMessage
import django.dispatch

new_comment_signal = django.dispatch.Signal()
del_comment_signal = django.dispatch.Signal()

def make_letter(profile, template, context):
    from src.core.models import Letter
    t = loader.get_template('email/' + template)
    c = Context(context)
    subject, content = t.render(c).split("\n", 1)
    letter = Letter(recipient=profile, subject=subject, content=content)
    letter.save()

def notice_admin(sender, **kwargs):
    message = EmailMessage(u"Новый комментарий", 
                           '<a href="http://uralsocionics.ru%s">%s</a>' % (sender.content_object.get_absolute_url(), sender.content_object.title),
                           'robot@uralsocionics.ru', 
                           ['madera@socion.org'])
    message.content_subtype = "html"
    message.send(fail_silently=False)
    
def increase_comments_count(sender, **kwargs):
    sender.content_object.comments_count += 1
    sender.content_object.save()
            
def decrease_comments_count(sender, **kwargs):
    sender.content_object.comments_count -= 1
    sender.content_object.save()            
            
new_comment_signal.connect(increase_comments_count)
new_comment_signal.connect(notice_admin)
del_comment_signal.connect(decrease_comments_count)            