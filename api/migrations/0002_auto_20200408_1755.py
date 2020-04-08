# Generated by Django 3.0.5 on 2020-04-08 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('auto_fb_post_mode', models.BooleanField()),
                ('currencycode', models.TextField()),
                ('goal', models.IntegerField()),
                ('donators', models.IntegerField()),
                ('days_active', models.IntegerField()),
                ('has_beneficiary', models.BooleanField()),
                ('status', models.BooleanField()),
                ('deactivated', models.BooleanField()),
                ('campaign_hearts', models.IntegerField()),
                ('social_share_total', models.IntegerField()),
                ('location_country', models.TextField()),
                ('is_charity', models.BooleanField()),
                ('charity_valid', models.BooleanField()),
                ('avg_donation', models.DecimalField(decimal_places=2, max_digits=10)),
                ('c_rating', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]