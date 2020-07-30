# Generated by Django 3.0.8 on 2020-07-30 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='title',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='album',
            name='cover_photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cover_for', to='core.Photo'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='caption',
            field=models.TextField(blank=True, null=True),
        ),
    ]