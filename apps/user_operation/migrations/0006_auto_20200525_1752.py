# Generated by Django 3.0.6 on 2020-05-25 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0005_auto_20200525_1739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userleavingmessage',
            old_name='msg_type',
            new_name='message_type',
        ),
    ]
