# Generated by Django 4.0.1 on 2022-10-12 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_alter_groupuser_group_id_alter_groupuser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupuser',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.group'),
        ),
        migrations.AlterField(
            model_name='groupuser',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]