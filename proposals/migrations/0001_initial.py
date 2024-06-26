# Generated by Django 5.0 on 2024-04-01 09:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_alter_user_groups_alter_user_user_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('approved', 'Approoved')], default='pending', max_length=20)),
                ('assigned', models.CharField(choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('approved', 'Approoved')], default='pending', max_length=20)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('proposer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=50)),
                ('marks', models.IntegerField()),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposals.proposal')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.category')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('marks', models.IntegerField()),
                ('max_words', models.IntegerField(blank=True, null=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposals.template')),
            ],
        ),
        migrations.AddField(
            model_name='proposal',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposals.template'),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposals.proposal')),
            ],
            options={
                'unique_together': {('proposal', 'reviewer')},
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposals.proposal')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposals.question')),
            ],
            options={
                'unique_together': {('proposal', 'question')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='proposal',
            unique_together={('template', 'proposer')},
        ),
    ]
