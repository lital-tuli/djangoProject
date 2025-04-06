# Generated by Django 5.1.6 on 2025-04-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_author_alter_article_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', help_text='Publication status of the article', max_length=10),
        ),
    ]
