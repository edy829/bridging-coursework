# Generated by Django 3.0.6 on 2020-05-21 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField()),
                ('education', models.TextField()),
                ('experience', models.TextField()),
                ('other', models.TextField()),
            ],
        ),
    ]
