# Generated by Django 5.1.3 on 2025-03-13 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_transaction_account_transaction_target_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default=12344321, max_length=128, verbose_name='密码'),
            preserve_default=False,
        ),
    ]
