# Generated by Django 4.2.5 on 2023-10-14 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='following',
        ),
    ]