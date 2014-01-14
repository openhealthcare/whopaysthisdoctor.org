# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'GrantBenefit.amount'
        db.delete_column(u'doctors_grantbenefit', 'amount')

        # Adding field 'GrantBenefit.band'
        db.add_column(u'doctors_grantbenefit', 'band',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'OtherMedicalBenefit.amount'
        db.delete_column(u'doctors_othermedicalbenefit', 'amount')

        # Adding field 'OtherMedicalBenefit.band'
        db.add_column(u'doctors_othermedicalbenefit', 'band',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'FeeBenefit.amount'
        db.delete_column(u'doctors_feebenefit', 'amount')

        # Adding field 'FeeBenefit.band'
        db.add_column(u'doctors_feebenefit', 'band',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'PharmaBenefit.amount'
        db.delete_column(u'doctors_pharmabenefit', 'amount')

        # Adding field 'PharmaBenefit.band'
        db.add_column(u'doctors_pharmabenefit', 'band',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'GrantBenefit.amount'
        raise RuntimeError("Cannot reverse this migration. 'GrantBenefit.amount' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'GrantBenefit.amount'
        db.add_column(u'doctors_grantbenefit', 'amount',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)

        # Deleting field 'GrantBenefit.band'
        db.delete_column(u'doctors_grantbenefit', 'band')


        # User chose to not deal with backwards NULL issues for 'OtherMedicalBenefit.amount'
        raise RuntimeError("Cannot reverse this migration. 'OtherMedicalBenefit.amount' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'OtherMedicalBenefit.amount'
        db.add_column(u'doctors_othermedicalbenefit', 'amount',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)

        # Deleting field 'OtherMedicalBenefit.band'
        db.delete_column(u'doctors_othermedicalbenefit', 'band')


        # User chose to not deal with backwards NULL issues for 'FeeBenefit.amount'
        raise RuntimeError("Cannot reverse this migration. 'FeeBenefit.amount' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'FeeBenefit.amount'
        db.add_column(u'doctors_feebenefit', 'amount',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)

        # Deleting field 'FeeBenefit.band'
        db.delete_column(u'doctors_feebenefit', 'band')


        # User chose to not deal with backwards NULL issues for 'PharmaBenefit.amount'
        raise RuntimeError("Cannot reverse this migration. 'PharmaBenefit.amount' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PharmaBenefit.amount'
        db.add_column(u'doctors_pharmabenefit', 'amount',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)

        # Deleting field 'PharmaBenefit.band'
        db.delete_column(u'doctors_pharmabenefit', 'band')


    models = {
        u'doctors.declaration': {
            'Meta': {'object_name': 'Declaration'},
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 1, 14, 0, 0)'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['doctors.Doctor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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