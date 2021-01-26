# Generated by Django 3.0.11 on 2021-01-22 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20210122_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityattributes',
            name='restriction',
            field=models.ForeignKey(blank=True, help_text="If added this atribute will be 'restriction' significant only. Eg. WT room for Bronze members only", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restriction', to='members.Metadata'),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('member', 'community')},
        ),
    ]