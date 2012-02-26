# -*- coding: utf-8 -*-
import calendar
from datetime import date, timedelta

from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext, Context, loader
from django.core.mail import EmailMessage
from tagging.models import Tag, TaggedItem
from django_subscribe.models import Subscription

from core.models import *
from core.forms import *

def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    if not context_dict:
        context_dict = {}
    context_dict['request'] = request
    context = RequestContext(request, context_dict)
    return _render_to_response(template_name, context_instance=context)


def index(request):
    context = {'articles': Article.objects.order_by('-date_created')[:7],
               'admin': request.user.is_superuser,
               }
    return render_to_response(request, 'index.html', context)

def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    articles = category.categories.order_by('-date_created')
    context = {'category': category,
               'last_articles': articles[:category.announce_amount],
               'articles': articles[category.announce_amount:],
               'children': Category.objects.filter(parent=category)
               }
    return render_to_response(request, 'category.html', context)

def article(request, article_id):
    profile = request.user.is_authenticated() and request.user.get_profile() or None
    context = {'article': get_object_or_404(Article, pk=article_id)
               }

    if request.user.is_authenticated():
        if request.POST.get('action'):
            # Сохраняем коммент
            content = request.POST.get('content')
            if len(content) > 0:
                context['article'].comments.create(author=profile, content=content)
                return HttpResponseRedirect(reverse('article', args=[article_id]))
            else:
                context['error'] = u"Вы забыли ввести комментарий"

    return render_to_response(request, 'article.html', context)

def edition(request, edition_id):
    edition = get_object_or_404(Edition, pk=edition_id)
    context = {'edition': edition,
               'articles': edition.article_set.all()
               }
    return render_to_response(request, 'edition.html', context)

def tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    context = {'tag': tag,
               'articles': TaggedItem.objects.get_by_model(Article, [tag])
               }
    return render_to_response(request, 'tag.html', context)


def schedule(request):
    months_count = 2
    schedule = []
    today = date.today()
    request_date = today
    if 'date' in request.GET:
        try:
            request_date = date( *time.strptime(request.GET['date'], "%Y-%m-%d")[:3] )
            if request_date < date(2009, 1, 1):
                request_date = date.today()
        except ValueError:
            pass

    request_date = request_date.replace(day=1)
    startMonth = request_date.month
    days = dict( (d.date, d) for d in EventDay.objects.filter(date__range=(request_date, request_date+timedelta(days=100)) ) )
    for m in xrange(startMonth, startMonth+months_count):
        if m > 12:
            month = m - 12
            year = request_date.year + 1
        else:
            month = m
            year = request_date.year

        month_days = calendar.monthcalendar(year, month)

        for week in month_days:
            for i in xrange(0, len(week)):
                week[i] = {'day':week[i]}
                try:
                    week[i]['date'] = date(year, month, int(week[i]['day']))
                    if i >= 5:
                        week[i]['holiday'] = True
                    if today == week[i]['date']:
                        week[i]['today'] = True
                    week[i]['event'] = days.get(week[i]['date'])
                except ValueError:
                    week[i]['date'] = ''

        schedule.append({'month':month_days, 'number':month})

    return render_to_response(request, 'schedule.html',
                              {'schedule':schedule,
                               'prev': (request_date - timedelta(days=15)).replace(day=1),
                               'next': (request_date + timedelta(days=45)).replace(day=1)
                               })

def order(request):
    context = {}
    if request.POST:
        context['form'] = OrderForm(request.POST)
        if context['form'].is_valid():
            message = EmailMessage(u"Заказ",
                                   context['form'].cleaned_data['contacts'] + "\n\n" + context['form'].cleaned_data['order'],
                                   'order@uralsocionics.ru',
                                   ['madera@socion.org'])
            message.send()
            context['error'] = u"Ваш заказ принят"
        else:
            context['error'] = context['form'].str_errors()
    else:
        context['error'] = u"заполните форму заказа"

    return render_to_response(request, 'order.html', context)


def ask(request):
    if 'done' in request.GET:
        return render_to_response(request, 'thanks.html')

    elif request.POST:
        form = Ask01(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ask') + '?done=1')

    else:
        form = Ask01()

    return render_to_response(request, 'ask.html', {'form':form})


def sitemap(request):
    context = {'editions': Edition.objects.all(),
               'categories': Category.objects.all(),
               'articles': Article.objects.all()
               }
    return render_to_response(request, 'sitemap.html', context)

def send_registration_letter(profile):
    t = loader.get_template('email/registration.html')
    c = Context({'profile':profile})
    subject, content = t.render(c).split("\n", 1)
    letter = Letter(recipient=profile, subject=subject, content=content)
    letter.save()

def registration(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(form.cleaned_data['username'],
                                                form.cleaned_data['email'],
                                                form.cleaned_data['password'])
            new_user.is_active = True
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            auth.login(request, user)

            profile = Profile(user=new_user,
                              nick=form.cleaned_data['username'])
            profile.save()

            send_registration_letter(profile)

            s = Subscription(email=form.cleaned_data['email'])
            s.fill_codes()
            s.confirm(s.confirmation_code)

            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm(initial={})

    return render_to_response(request, 'registration.html', {'form':form})
