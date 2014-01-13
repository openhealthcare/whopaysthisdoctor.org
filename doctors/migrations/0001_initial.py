# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Doctor'
        db.create_table(u'doctors_doctor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('gmc_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('primary_employer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('employment_address', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'doctors', ['Doctor'])

        # Adding model 'Declaration'
        db.create_table(u'doctors_declaration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('interests', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('past_declarations', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('other_declarations', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 1, 3, 0, 0))),
        ))
        db.send_create_signal(u'doctors', ['Declaration'])

        # Adding model 'PharmaBenefit'
        db.create_table(u'doctors_pharmabenefit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('declaration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Declaration'], null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'doctors', ['PharmaBenefit'])

        # Adding model 'OtherMedicalBenefit'
        db.create_table(u'doctors_othermedicalbenefit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('declaration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Declaration'], null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'doctors', ['OtherMedicalBenefit'])

        # Adding model 'FeeBenefit'
        db.create_table(u'doctors_feebenefit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('declaration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Declaration'], null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'doctors', ['FeeBenefit'])

        # Adding model 'GrantBenefit'
        db.create_table(u'doctors_grantbenefit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('declaration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Declaration'], null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'doctors', ['GrantBenefit'])


    def backwards(self, orm):
        # Deleting model 'Doctor'
        db.delete_table(u'doctors_doctor')

        # Deleting model 'Declaration'
        db.delete_table(u'doctors_declaration')

        # Deleting model 'PharmaBenefit'
        db.delete_table(u'doctors_pharmabenefit')

        # Deleting model 'OtherMedicalBenefit'
        db.delete_table(u'doctors_othermedicalbenefit')

        # Deleting model 'FeeBenefit'
        db.delete_table(u'doctors_feebenefit')

        # Deleting model 'GrantBenefit'
        db.delete_table(u'doctors_grantbenefit')


    models = {
        u'doctors.declaration': {
            'Meta': {'object_name': 'Declaration'},
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 1, 3, 0, 0)'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'other_declarations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'past_declarations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'doctors.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'employment_address': ('django.db.models.fields.TextField', [], {}),
            'gmc_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'primary_employer': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'doctors.feebenefit': {
            'Meta': {'object_name': 'FeeBenefit'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'declaration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Declaration']", 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'doctors.grantbenefit': {
            'Meta': {'object_name': 'GrantBenefit'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'declaration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Declaration']", 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'doctors.othermedicalbenefit': {
            'Meta': {'object_name': 'OtherMedicalBenefit'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'declaration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Declaration']", 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'doctors.pharmabenefit': {
            'Meta': {'object_name': 'PharmaBenefit'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'declaration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Declaration']", 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['doctors']