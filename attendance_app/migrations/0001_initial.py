# Generated by Django 3.2.13 on 2022-05-24 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTable',
            fields=[
                ('class_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=255)),
                ('meet_link', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('class_date', models.DateField()),
                ('ludt', models.DateTimeField(auto_now_add=True)),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('att_id', models.AutoField(primary_key=True, serialize=False)),
                ('joining_verification', models.BooleanField(default=False)),
                ('leaving_verification', models.BooleanField(default=False)),
                ('attended', models.BooleanField(default=False)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='attendance_app.classtable')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
