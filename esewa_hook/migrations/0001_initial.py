# Generated by Django 3.0 on 2021-05-27 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_auto_20210527_0509'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EsewaPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('payment_method', models.CharField(choices=[['ESEWA', 'ESEWA']], default='ESEWA', max_length=10)),
                ('card_number', models.CharField(default='none', max_length=200)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='esewa_payment_customer', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='esewa_payment_order', to='store.Order')),
            ],
        ),
        migrations.CreateModel(
            name='EsewaOrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='John Doe', max_length=200)),
                ('phone_number', models.IntegerField(default=0)),
                ('email', models.EmailField(default='test@gmail.com', max_length=254)),
                ('delivery_address', models.CharField(default='Street Address', max_length=200)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('payment_object', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='esewa_hook.EsewaPayment')),
            ],
        ),
    ]
