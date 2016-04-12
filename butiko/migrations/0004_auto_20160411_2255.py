# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 02:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('butiko', '0003_auto_20160406_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permrequest',
            name='itemList',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_requests', to='butiko.ItemList'),
        ),
        migrations.AlterField(
            model_name='permrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]