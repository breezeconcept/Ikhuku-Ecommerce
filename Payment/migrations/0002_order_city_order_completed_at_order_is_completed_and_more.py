# Generated by Django 5.0 on 2024-01-02 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0001_initial'),
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='Products.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to='order_receipt/'),
        ),
        migrations.AddField(
            model_name='order',
            name='reference',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='street_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
