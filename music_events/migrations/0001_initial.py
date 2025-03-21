# Generated by Django 4.2.19 on 2025-02-17 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('UID', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=10)),
                ('showUnit', models.CharField(blank=True, max_length=255, null=True)),
                ('discountInfo', models.TextField(blank=True, null=True)),
                ('descriptionFilterHtml', models.TextField(blank=True, null=True)),
                ('imageUrl', models.URLField(blank=True, null=True)),
                ('masterUnit', models.JSONField(blank=True, null=True)),
                ('subUnit', models.JSONField(blank=True, null=True)),
                ('supportUnit', models.JSONField(blank=True, null=True)),
                ('otherUnit', models.JSONField(blank=True, null=True)),
                ('webSales', models.URLField(blank=True, null=True)),
                ('sourceWebPromote', models.URLField(blank=True, null=True)),
                ('sourceWebName', models.CharField(blank=True, max_length=255, null=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('hitRate', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True, null=True)),
                ('editModifyDate', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('locationID', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255)),
                ('locationName', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShowInfo',
            fields=[
                ('showID', models.AutoField(primary_key=True, serialize=False)),
                ('show_time', models.DateTimeField()),
                ('endTime', models.DateTimeField(blank=True, null=True)),
                ('onSales', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=1)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_info', to='music_events.event')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_info', to='music_events.location')),
            ],
        ),
    ]
