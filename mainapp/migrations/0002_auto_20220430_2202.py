# Generated by Django 3.2.13 on 2022-04-30 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='question_text',
            new_name='word',
        ),
        migrations.RemoveField(
            model_name='word',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='word',
            name='image',
            field=models.ImageField(null=True, upload_to='mainapp'),
        ),
        migrations.AlterField(
            model_name='word',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
