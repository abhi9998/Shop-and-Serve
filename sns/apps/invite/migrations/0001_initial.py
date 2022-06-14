# Generated by Django 3.2.12 on 2022-03-29 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createAt', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('groupid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.group')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'invite',
            },
        ),
    ]
