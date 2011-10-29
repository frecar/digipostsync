# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'DropboxToken.request_token'
        db.delete_column('dropbox_dropboxtoken', 'request_token')

        # Adding field 'DropboxToken.request_token_key'
        db.add_column('dropbox_dropboxtoken', 'request_token_key', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)

        # Adding field 'DropboxToken.request_token_secret'
        db.add_column('dropbox_dropboxtoken', 'request_token_secret', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'DropboxToken.request_token'
        db.add_column('dropbox_dropboxtoken', 'request_token', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)

        # Deleting field 'DropboxToken.request_token_key'
        db.delete_column('dropbox_dropboxtoken', 'request_token_key')

        # Deleting field 'DropboxToken.request_token_secret'
        db.delete_column('dropbox_dropboxtoken', 'request_token_secret')


    models = {
        'dropbox.dropboxtoken': {
            'Meta': {'object_name': 'DropboxToken'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_token_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'request_token_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'token'", 'to': "orm['user.User']"})
        },
        'user.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['dropbox']
