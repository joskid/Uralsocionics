# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Profile'
        db.create_table('core_profile', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nick', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='socionics_profile', primary_key=True, to=orm['auth.User'])),
            ('icq', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1000, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal('core', ['Profile'])

        # Adding model 'Comment'
        db.create_table('core_comment', (
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Profile'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['Comment'])

        # Adding model 'Letter'
        db.create_table('core_letter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Profile'])),
            ('date_sended', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Letter'])

        # Adding model 'Edition'
        db.create_table('core_edition', (
            ('price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Edition'])

        # Adding model 'Category'
        db.create_table('core_category', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', blank=True, null=True, to=orm['core.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('show_title', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('announce_amount', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Category'])

        # Adding model 'Article'
        db.create_table('core_article', (
            ('comments_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('other_author', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('comments', self.gf('django.contrib.contenttypes.generic.GenericRelation')(to=orm['core.Comment'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Edition'], null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comments_enabled', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('announce', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Article'])

        # Adding M2M table for field category on 'Article'
        db.create_table('core_article_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['core.article'], null=False)),
            ('category', models.ForeignKey(orm['core.category'], null=False))
        ))

        # Adding M2M table for field authors on 'Article'
        db.create_table('core_article_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['core.article'], null=False)),
            ('profile', models.ForeignKey(orm['core.profile'], null=False))
        ))

        # Adding model 'Illustration'
        db.create_table('core_illustration', (
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Article'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Illustration'])

        # Adding model 'EventDay'
        db.create_table('core_eventday', (
            ('date', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('core', ['EventDay'])

    def backwards(self, orm):

        # Deleting model 'Profile'
        db.delete_table('core_profile')

        # Deleting model 'Comment'
        db.delete_table('core_comment')

        # Deleting model 'Letter'
        db.delete_table('core_letter')

        # Deleting model 'Edition'
        db.delete_table('core_edition')

        # Deleting model 'Category'
        db.delete_table('core_category')

        # Deleting model 'Article'
        db.delete_table('core_article')

        # Removing M2M table for field category on 'Article'
        db.delete_table('core_article_category')

        # Removing M2M table for field authors on 'Article'
        db.delete_table('core_article_authors')

        # Deleting model 'Illustration'
        db.delete_table('core_illustration')

        # Deleting model 'EventDay'
        db.delete_table('core_eventday')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.article': {
            'Meta': {'object_name': 'Article'},
            'announce': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'authors'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Profile']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Category']"}),
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['core.Comment']"}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Edition']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'other_author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.category': {
            'Meta': {'object_name': 'Category'},
            'announce_amount': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'blank': 'True', 'null': 'True', 'to': "orm['core.Category']"}),
            'show_title': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Profile']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'core.edition': {
            'Meta': {'object_name': 'Edition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.eventday': {
            'Meta': {'object_name': 'EventDay'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.illustration': {
            'Meta': {'object_name': 'Illustration'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.letter': {
            'Meta': {'object_name': 'Letter'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_sended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Profile']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.profile': {
            'Meta': {'object_name': 'Profile'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'icq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1000', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'socionics_profile'", 'primary_key': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['core']
