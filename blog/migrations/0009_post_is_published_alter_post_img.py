# Generated by Django 5.1.7 on 2025-04-01 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(null=True, upload_to='post/images/'),
        ),
    ]
