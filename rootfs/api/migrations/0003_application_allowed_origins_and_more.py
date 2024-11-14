# Generated by Django 4.2.16 on 2024-11-14 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='allowed_origins',
            field=models.TextField(blank=True, default='', help_text='Allowed origins list to enable CORS, space separated'),
        ),
        migrations.AddField(
            model_name='application',
            name='hash_client_secret',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='post_logout_redirect_uris',
            field=models.TextField(blank=True, default='', help_text='Allowed Post Logout URIs list, space separated'),
        ),
    ]
