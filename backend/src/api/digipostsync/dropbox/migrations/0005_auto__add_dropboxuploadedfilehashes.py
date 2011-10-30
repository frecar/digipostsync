# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DropboxUploadedFileHashes'
        db.create_table('dropbox_dropboxuploadedfilehashes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dropbox_file_hashes', to=orm['user.User'])),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('dropbox', ['DropboxUploadedFileHashes'])


    def backwards(self, orm):
        
        # Deleting model 'DropboxUploadedFileHashes'
        db.delete_table('dropbox_dropboxuploadedfilehashes')


    models = {
        'dropbox.dropboxtoken': {
            'Meta': {'object_name': 'DropboxToken'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'token'", 'to': "orm['user.User']"})
        },
        'dropbox.dropboxuploadedfilehashes': {
            'Meta': {'object_name': 'DropboxUploadedFileHashes'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dropbox_file_hashes'", 'to': "orm['user.User']"})
        },
        'user.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['dropbox']
