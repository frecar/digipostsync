# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('user_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('user', ['User'])


    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('user_user')


    models = {
        'user.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['user']
