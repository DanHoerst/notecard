# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Semester'
        db.create_table('notecards_semester', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('semester_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('notecards', ['Semester'])

        # Adding model 'Section'
        db.create_table('notecards_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notecards.Semester'])),
        ))
        db.send_create_signal('notecards', ['Section'])

        # Adding model 'Notecard'
        db.create_table('notecards_notecard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notecard_name', self.gf('django.db.models.fields.TextField')()),
            ('notecard_body', self.gf('django.db.models.fields.TextField')()),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notecards.Section'])),
            ('known', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('notecards', ['Notecard'])

    def backwards(self, orm):
        # Deleting model 'Semester'
        db.delete_table('notecards_semester')

        # Deleting model 'Section'
        db.delete_table('notecards_section')

        # Deleting model 'Notecard'
        db.delete_table('notecards_notecard')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notecards.notecard': {
            'Meta': {'object_name': 'Notecard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'known': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notecard_body': ('django.db.models.fields.TextField', [], {}),
            'notecard_name': ('django.db.models.fields.TextField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notecards.Section']"})
        },
        'notecards.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notecards.Semester']"})
        },
        'notecards.semester': {
            'Meta': {'object_name': 'Semester'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['notecards']