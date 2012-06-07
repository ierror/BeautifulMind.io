# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MindMap', fields ['slug']
        db.delete_unique('mindmap_mindmap', ['slug'])


    def backwards(self, orm):
        # Adding unique constraint on 'MindMap', fields ['slug']
        db.create_unique('mindmap_mindmap', ['slug'])


    models = {
        'mindmap.mindmap': {
            'Meta': {'object_name': 'MindMap'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'root_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mindmap.MindMapComponent']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '300'})
        },
        'mindmap.mindmapcomponent': {
            'Meta': {'object_name': 'MindMapComponent'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['mindmap.MindMapComponent']"}),
            'pos_left': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pos_top': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['mindmap']