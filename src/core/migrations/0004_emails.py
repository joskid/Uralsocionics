# encoding: utf-8
import datetime
import os
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings

from django_subscribe.models import Subscription


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        for email in open(os.path.join(os.path.dirname(__file__), 'emails.txt')).read().split(';'):
            s = Subscription(email=email.strip())
            s.fill_codes()
            s.confirm(s.confirmation_code)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'subscribe.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'confirmation_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'delete_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['subscribe']
