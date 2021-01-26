# Generated by Django 3.0.11 on 2021-01-19 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_community_communityattributes_membership_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership', to='members.Member'),
        ),
    ]