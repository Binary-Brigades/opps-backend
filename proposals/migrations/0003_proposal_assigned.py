# Generated by Django 5.0 on 2024-04-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_remove_proposal_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='assigned',
            field=models.BooleanField(default=False),
        ),
    ]
