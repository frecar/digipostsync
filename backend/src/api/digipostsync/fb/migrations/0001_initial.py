# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FacebookToken'
        db.create_table('fb_facebooktoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fb_token', to=orm['user.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('request_token', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
        ))
        db.send_create_signal('fb', ['FacebookToken'])


    def backwards(self, orm):
        
        # Deleting model 'FacebookToken'
        db.delete_table('fb_facebooktoken')


    models = {
        'fb.facebooktoken': {
            'Meta': {'object_name': 'FacebookToken'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fb_token'", 'to': "orm['user.User']"})
        },
        'user.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['fb']
