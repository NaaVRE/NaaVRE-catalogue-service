# Generated by Django 5.1.2 on 2024-10-16 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base_assets', '0001_initial'),
        ]

    operations = [
        migrations.CreateModel(
            name='BaseImage',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID'
                    )),
                ('build', models.CharField(
                    blank=True,
                    help_text='Build stage base image (eg: ghcr.io/qcdis/naavre/naavre-cell-build-python:v0.18)',
                    max_length=300
                    )),
                ('runtime', models.CharField(
                    blank=True,
                    help_text='Runtime stage base image (eg: ghcr.io/qcdis/naavre/naavre-cell-runtime-python:v0.18)',
                    max_length=300
                    )),
                ],
            ),
        migrations.CreateModel(
            name='BaseVariable',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID'
                    )),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(
                    choices=[('int', 'Integer'), ('float', 'Float'),
                             ('str', 'String'), ('list', 'List')],
                    max_length=100
                    )),
                ],
            ),
        migrations.CreateModel(
            name='Conf',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID'
                    )),
                ('name', models.CharField(max_length=100)),
                ('assignation', models.CharField(max_length=300)),
                ],
            ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID'
                    )),
                ('name', models.CharField(max_length=100)),
                ('module', models.CharField(blank=True, max_length=100)),
                ('asname', models.CharField(blank=True, max_length=100)),
                ],
            options={
                'verbose_name_plural': 'dependencies',
                },
            ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('basevariable_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True, primary_key=True, serialize=False,
                    to='workflow_cells.basevariable'
                    )),
                ],
            bases=('workflow_cells.basevariable',),
            ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('basevariable_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True, primary_key=True, serialize=False,
                    to='workflow_cells.basevariable'
                    )),
                ],
            bases=('workflow_cells.basevariable',),
            ),
        migrations.CreateModel(
            name='Param',
            fields=[
                ('basevariable_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True, primary_key=True, serialize=False,
                    to='workflow_cells.basevariable'
                    )),
                (
                    'default_value', models.CharField(blank=True, max_length=300)
                    ),
                ],
            bases=('workflow_cells.basevariable',),
            ),
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('basevariable_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True, primary_key=True, serialize=False,
                    to='workflow_cells.basevariable'
                    )),
                ],
            bases=('workflow_cells.basevariable',),
            ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('baseasset_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True, primary_key=True, serialize=False,
                    to='base_assets.baseasset'
                    )),
                ('container_image', models.CharField(
                    help_text=('Containerized cell image (example: '
                               'ghcr.io/qcdis/naavre-cells-test-2/print-msg-dev-user-name-at-domain-com:49c621b)'),
                    max_length=300
                    )),
                ('kernel', models.CharField(
                    blank=True,
                    help_text='Jupyter kernel of the source cell (example: ipython)',
                    max_length=100
                    )),
                ('source_url', models.URLField(
                    blank=True,
                    help_text=('URL of the folder on GitHub containing the sources of the image '
                               '(example: https://github.com/QCDIS/NaaVRE-cells-test-2/tree/'
                               '3262643c5800ea03d494fda7360fc617fd0309e1/print-msg-dev-user-name-at-domain-com)')
                    )),
                ('base_container_image', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.PROTECT,
                    to='workflow_cells.baseimage'
                    )),
                ('confs',
                 models.ManyToManyField(blank=True, to='workflow_cells.conf')),
                ('dependencies', models.ManyToManyField(
                    blank=True, to='workflow_cells.dependency'
                    )),
                ('inputs', models.ManyToManyField(
                    blank=True, to='workflow_cells.input'
                    )),
                ('outputs', models.ManyToManyField(
                    blank=True, to='workflow_cells.output'
                    )),
                ('params', models.ManyToManyField(
                    blank=True, to='workflow_cells.param'
                    )),
                ('secrets', models.ManyToManyField(
                    blank=True, to='workflow_cells.secret'
                    )),
                ],
            bases=('base_assets.baseasset',),
            ),
        ]
