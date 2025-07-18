# Generated by Django 5.1.7 on 2025-05-03 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('virtual_labs', '0003_virtuallab_image'),
        ]

    operations = [
        migrations.CreateModel(
            name='VirtualLabInstance',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID'
                    )),
                ('username', models.CharField(max_length=100, null=True)),
                ('virtual_lab', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.CASCADE,
                    to='virtual_labs.virtuallab'
                    )),
                ],
            ),
        ]
