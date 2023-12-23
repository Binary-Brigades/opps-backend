# Generated by Django 4.2.7 on 2023-12-16 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.category'),
        ),
    ]
