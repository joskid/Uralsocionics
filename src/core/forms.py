# -*- coding: utf-8 -*-
import re
from django.forms import *
from django.contrib.auth.models import User
from django.core.mail import send_mail


class CommonForm(Form):
    def errors_list(self):
        return [unicode(message) for k, l in self.errors.items() for message in l]

    def str_errors(self, divider=u". "):
        return divider.join(self.errors_list())


class RegistrationForm(CommonForm):
    username = CharField(label=u'Логин', help_text=u'Англ буквы и цифры, не менее 3 символов', error_messages={'required': u'Укажите желаемый логин'})
    password = CharField(required=False, max_length=100)
    password1 = CharField(max_length=100, widget=PasswordInput, error_messages={'required': u'Введите пароль'})
    password2 = CharField(max_length=100, widget=PasswordInput, error_messages={'required': u'Введите пароль повторно'})
    email = EmailField(max_length=100, error_messages={'required': u'Укажите свой email'})

    def clean_username(self):
        result = re.search(u'(.{3,})', self.cleaned_data['username'], re.I)
        if result:
            username = result.group(1)
            user = User.objects.filter(username=username)
            if len(user) > 0:
                raise ValidationError(u'Такой логин уже занят')

            return username
        else:
            raise ValidationError(u'Логин должен состоять из англ букв и цифр, не менее 3 символов')

    def clean_email(self):
        users = User.objects.filter(email=self.cleaned_data['email'])
        if len(users) > 0:
            raise ValidationError(u'Пользователь с такой почтой уже зарегистрирован')
        return self.cleaned_data['email']

    def clean(self):
        p1 = self.cleaned_data.get('password1', '')
        p2 = self.cleaned_data.get('password2', '')
        if not p1 == p2:
            raise ValidationError(u'Введенные пароли не одинаковые')

        self.cleaned_data['password'] = p1
        return self.cleaned_data


class OrderForm(CommonForm):
    order = CharField(label=u'Я хочу заказать', error_messages={'required': u'Вы не написали, что хотите заказать'},
                         widget=Textarea(attrs={'cols': 70, 'rows': 4}))
    contacts = CharField(label=u'Мои контакты (e-mail или телефон)', error_messages={'required': u'Укажите, как с вами связаться'},
                         widget=TextInput)


class Ask01(CommonForm):
    tim = CharField(label=u'Ваш ТИМ', error_messages={'required': u'Укажите ваш ТИМ'})
    selfmark = ChoiceField(label=u'Как изменилась после ознакомления с ТИМом Ваша самооценка?',
                           choices=(('up', u'Повысилась'),
                                    ('down', u'Понизилась'),
                                    ('stay', u'Не изменилась'),)
                           )
    selfglad = ChoiceField(label=u'Нравится ли Вам Ваш ТИМ?',
                           choices=(('yep', u'Да'),
                                    ('nope', u'Нет'))
                           )
    wantchange = ChoiceField(label=u'Хотели бы Вы иметь другой ТИМ?',
                           choices=(('yep', u'Да'),
                                    ('nope', u'Нет'))
                           )
    future = ChoiceField(label=u'Как Вы оцениваете Ваши перспективы и возможности с учетом ТИМа?',
                           choices=(('down', u'До знакомства с ТИМом выше, чем после'),
                                    ('up', u'До знакомства с ТИМом ниже, чем после'),
                                    ('stay', u'Одинаково'))
                           )

    def clean(self):
        print self.cleaned_data
        for name, f in self.base_fields.items():
            if isinstance(f, ChoiceField):
                for k, v in f.choices:
                    if k == self.cleaned_data[name]:
                        self.cleaned_data[name] = v

        return self.cleaned_data

    def save(self):
        message = "\n".join("%s: %s" % (f.label, self.cleaned_data[name]) for name, f in self.base_fields.items())
        send_mail(u"Опрос", message, 'ask@uralsocionics.ru', ['glader@glader.ru', 'madera@socion.org'])
