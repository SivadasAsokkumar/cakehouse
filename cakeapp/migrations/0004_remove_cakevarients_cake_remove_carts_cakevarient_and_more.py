# Generated by Django 4.1.4 on 2023-10-15 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cakeapp', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cakevarients',
            name='cake',
        ),
        migrations.RemoveField(
            model_name='carts',
            name='cakevarient',
        ),
        migrations.RemoveField(
            model_name='carts',
            name='user',
        ),
        migrations.RemoveField(
            model_name='offers',
            name='cakevarient',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='cakevarient',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='cakevarient',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Cakes',
        ),
        migrations.DeleteModel(
            name='CakeVarients',
        ),
        migrations.DeleteModel(
            name='Carts',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Offers',
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
        migrations.DeleteModel(
            name='Reviews',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
