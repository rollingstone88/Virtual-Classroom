# Generated by Django 4.1.1 on 2022-11-13 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_alter_classroom_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0007_delete_articlecomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('file', models.ImageField(blank=True, upload_to='comment')),
                ('submission_time', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='articles.article')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='classroom.classroom')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
