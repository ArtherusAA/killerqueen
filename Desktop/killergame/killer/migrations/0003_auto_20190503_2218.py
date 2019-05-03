# Generated by Django 2.1.7 on 2019-05-03 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('killer', '0002_auto_20190406_1930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='score',
            new_name='kills',
        ),
        migrations.AddField(
            model_name='user',
            name='wins',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
