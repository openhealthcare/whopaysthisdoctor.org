# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImportedDoctorCompanyLink'
        db.create_table(u'doctors_importeddoctorcompanylink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doctors.Doctor'])),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('officer_link', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('company_link', self.gf('django.db.models.fields.URLField')(max_length=300)),
        ))
        db.send_create_signal(u'doctors', ['ImportedDoctorCompanyLink'])


    def backwards(self, orm):
        # Deleting model 'ImportedDoctorCompanyLink'
        db.delete_table(u'doctors_importeddoctorcompanylink')


    models = {
        u'doctors.declaration': {
            'Meta': {'object_name': 'Declaration'},
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2019, 6, 15, 0, 0)'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2019, 6, 15, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other_declarations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'past_declarations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'doctors.declarationlink': {
            'Meta': {'object_name': 'DeclarationLink'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2019, 6, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'6ae3b499'", 'unique': 'True', 'max_length': '64'})
        },
        u'doctors.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'employment_address': ('django.db.models.fields.TextField', [], {}),
            'gmc_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'primary_employer': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'doctors.feebenefit': {
            'Meta': {'object_name': 'FeeBenefit'},
            'band': ('django.db.models.fields.IntegerField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'declaration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Declaration']", 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'doctors.grantbenefit': {
            'Meta': {'object_name': 'GrantBenefit'},
            'band': ('django.db.models.fields.IntegerField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'declaration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Declaration']", 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'doctors.importeddoctorcompanylink': {
            'Meta': {'object_name': 'ImportedDoctorCompanyLink'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'company_link': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'officer_link': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        u'doctors.othermedicalbenefit': {
            'Meta': {'object_name': 'OtherMedicalBenefit'},
            'band': ('django.db.models.fields.IntegerField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'declaration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Declaration']", 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'doctors.pharmabenefit': {
            'Meta': {'object_name': 'PharmaBenefit'},
            'band': ('django.db.models.fields.IntegerField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'declaration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Declaration']", 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['doctors']