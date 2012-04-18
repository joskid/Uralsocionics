# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from tagging.fields import TagField

from core.signals import new_comment_signal, del_comment_signal

class GenericManager(models.Manager):
    """
    Filters query set with given selectors
    """
    def __init__(self, **kwargs):
        super(GenericManager, self).__init__()
        self.selectors = kwargs

    def get_query_set(self):
        return super(GenericManager, self).get_query_set().filter(**self.selectors)


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='socionics_profile', primary_key=True)
    name = models.CharField(null=True, max_length=200, verbose_name=u"ФИО")
    nick = models.CharField(null=True, max_length=200, blank=True, verbose_name=u"Игровое имя")
    description = models.TextField(null=True, blank=True, verbose_name=u"Описание")
    url = models.URLField(null=True, blank=True, verbose_name=u"Адрес")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"Телефон")
    birthdate = models.DateField(null=True, blank=True, verbose_name=u"Дата рождения")
    icq = models.IntegerField(null=True, blank=True, verbose_name="ICQ")
    order = models.IntegerField(null=True, blank=True, verbose_name=u"Порядок", default=1000)

    LEVEL_CHOICES = (
        ('0', 'Anonim'),
        ('10', 'Logged user'),
        ('20', 'Author'),
        ('60', 'Site admin'),
    )
    level = models.IntegerField(choices=LEVEL_CHOICES, default=10, verbose_name=u"Уровень")

    objects = GenericManager(level__gte=10)  # Зарегистрированные пользователи

    class Meta:
        verbose_name = u"Профиль юзера"
        verbose_name_plural = u"Профили юзеров"
        ordering = ['order']

    def __unicode__(self):
        return self.name or self.nick or ""

    def is_empowered(self):
        return self.level >= 20


class Comment(models.Model):
    """ Комментарии """
    author = models.ForeignKey(Profile, verbose_name=u"Автор")
    content = models.TextField(verbose_name=u"Содержание")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания", editable=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return self.content_object.title + ": " + self.content[:20]

    def get_absolute_url(self):
        return "%s#c%i" % (self.content_object.get_absolute_url(), self.id)

    def parent_title(self):
        return self.content_type.__unicode__() + ': ' + self.content_object.__unicode__()
    parent_title.short_description = u'Родитель'

    def save(self, **kwargs):
        try:
            c = Comment.objects.get(pk=self.id)
        except Comment.DoesNotExist:
            new_comment_signal.send(sender=self)
        super(Comment, self).save(**kwargs)

    def delete(self):
        del_comment_signal.send(sender=self)
        super(Comment, self).delete()

    class Meta:
        verbose_name = u"Комментарий"
        verbose_name_plural = u"Комментарии"
        ordering = ['date_created']


class Letter(models.Model):
    recipient = models.ForeignKey(Profile, verbose_name=u"Адресат")
    subject = models.CharField(max_length=200, verbose_name=u"Тема")
    content = models.TextField(verbose_name=u"Содержание")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")
    date_sended = models.DateTimeField(null=True, blank=True, verbose_name=u"Дата отправки")

    objects = GenericManager()
    waiting = GenericManager(date_sended=None)  # Ожидающие отправки

    def __unicode__(self):
        return "%s: %s" % (self.recipient, self.subject)


class Edition(models.Model):
    u""" Издание (журнал, книга, брошюра) """
    name = models.CharField(max_length=200, verbose_name=u"Название")
    number = models.CharField(max_length=20, verbose_name=u"Номер")
    price = models.IntegerField(verbose_name=u"Цена", null=True, blank=True,
                                help_text=u"Не указывайте цену, если издания нет в продаже")

    def __unicode__(self):
        return self.name + ' ' + self.number

    class Meta:
        verbose_name = u"Издание"
        verbose_name_plural = u"Издания"


class Category(models.Model):
    """ Разделы статей """
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Название")
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, verbose_name=u"Родительский раздел")
    description = models.TextField(null=True, blank=True, verbose_name=u"Описание")
    order = models.IntegerField(default=100, null=True, blank=True, verbose_name=u"Порядок")
    show_title = models.BooleanField(default=True, verbose_name=u"Показывать название")
    announce_amount = models.IntegerField(default=5, verbose_name=u"Количество анонсов")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Раздел статей"
        verbose_name_plural = u"Разделы статей"
        ordering = ['order']


class Article(models.Model):
    """ Статьи """
    category = models.ManyToManyField(Category, null=True, blank=True, related_name='categories', verbose_name=u"Категория")
    edition = models.ForeignKey(Edition, null=True, blank=True, verbose_name=u"Журнал")
    authors = models.ManyToManyField(Profile, null=True, blank=True, related_name='authors', verbose_name=u"Автор", limit_choices_to={'level__gte': 20})
    other_author = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Другой автор", help_text=u"Автор, не имеющий отношения к этому сайту. Просто имя. Можно перечислить несколько через запятую.")
    title = models.CharField(max_length=200, verbose_name=u"Название")
    slug = models.SlugField(max_length=200, null=True, blank=True, verbose_name=u"Англ. слово", help_text=u"Это слово будет краткой ссылкой на статью. Можно использовать англ. буквы и символ '_'.")
    announce = models.TextField(verbose_name=u"Анонс", null=True, blank=True)
    content = models.TextField(verbose_name=u"Содержание")
    comments_enabled = models.BooleanField(verbose_name=u"Комментарии разрешены", default=False)
    order = models.IntegerField(default=100, null=True, blank=True, verbose_name=u"Порядок")
    date_created = models.DateTimeField(default=datetime.now, verbose_name=u"Дата создания")
    last_modified = models.DateTimeField(auto_now=True, verbose_name=u"Дата последнего изменения", editable=False)
    comments_count = models.IntegerField(default=0, verbose_name=u"Количество комментариев", editable=False)
    show_date = models.BooleanField(default=True, verbose_name=u"Показывать дату страницы")
    show_share_block = models.BooleanField(default=True, verbose_name=u"Показывать социальные кнопки")

    comments = generic.GenericRelation(Comment)

    tags = TagField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/article/%d" % self.pk

    def all_authors(self):
        authors_list = list(self.authors.all()) or []
        if self.other_author:
            authors_list.append(self.other_author)
        return authors_list

    def save(self, *args, **kwargs):
        self.comments_count = self.comments.all().count()
        super(Article, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Статья"
        verbose_name_plural = u"Статьи"
        ordering = ['order', '-date_created']


class Illustration(models.Model):
    """ Картинки к статьям """
    article = models.ForeignKey(Article, verbose_name=u"Статья")
    title = models.CharField(max_length=200, verbose_name=u"Название", blank=True, default="")
    img = models.ImageField(
        verbose_name=u"Картинка",
        upload_to='img',
        null=True, blank=True, default=None,
        help_text="Чтобы вставить картинку в статью, скопируй правой кнопкой ссылку выше и напиши в статье &lt;img src=\"ссылка\"&gt;"
    )

    def __unicode__(self):
        return self.title

    def article_title(self):
        return self.article.title
    article_title.short_description = u'Статья'

    class Meta:
        verbose_name = u"Картинка"
        verbose_name_plural = u"Картинки"


class EventDay(models.Model):
    """ Даты расписания """
    date = models.DateField(verbose_name=u"Дата события", unique=True)
    content = models.TextField(verbose_name=u"Содержание")

    def __unicode__(self):
        return unicode(self.date)

    class Meta:
        verbose_name = u"Дата расписания"
        verbose_name_plural = u"Даты расписания"
