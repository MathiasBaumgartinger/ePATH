# Generated by Django 5.2.4 on 2025-07-17 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatbotresponse',
            old_name='response',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='chatusermessage',
            old_name='message',
            new_name='content',
        ),
    ]
