# Generated by Django 3.2.1 on 2021-05-10 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_contact_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('uno', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
            ],
        ),
    ]