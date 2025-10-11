# Generated manually to fix 'boos' role to 'boss'

from django.db import migrations


def fix_boos_to_boss(apps, schema_editor):
    """Update any existing users with role 'boos' to 'boss'."""
    Users = apps.get_model('users', 'Users')
    Users.objects.filter(role='boos').update(role='boss')


def reverse_fix_boos_to_boss(apps, schema_editor):
    """Reverse: change 'boss' back to 'boos'."""
    Users = apps.get_model('users', 'Users')
    Users.objects.filter(role='boss').update(role='boos')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_boos_to_boss, reverse_fix_boos_to_boss),
    ]
