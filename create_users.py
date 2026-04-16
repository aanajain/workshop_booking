from django.contrib.auth.models import User, Group
from workshop_app.models import Profile
import os

# Create Instructor Group
inst_group, _ = Group.objects.get_or_create(name='instructor')

# 1. Admin
admin_user, created = User.objects.get_or_create(username='admin')
if created or not admin_user.has_usable_password():
    admin_user.set_password('password123')
admin_user.is_superuser = True
admin_user.is_staff = True
admin_user.save()

# 2. Coordinator
coord_user, created = User.objects.get_or_create(username='coordinator')
if created or not coord_user.has_usable_password():
    coord_user.set_password('password123')
coord_user.first_name = "Test"
coord_user.last_name = "Coordinator"
coord_user.save()
Profile.objects.get_or_create(
    user=coord_user,
    defaults={
        'state': 'IN-MH',
        'institute': 'Dummy Institute',
        'department': 'computer engineering',
        'phone_number': '9999999999',
        'position': 'coordinator'
    }
)

# 3. Instructor
inst_user, created = User.objects.get_or_create(username='instructor')
if created or not inst_user.has_usable_password():
    inst_user.set_password('password123')
inst_user.first_name = "Test"
inst_user.last_name = "Instructor"
inst_user.save()
inst_user.groups.add(inst_group)
Profile.objects.get_or_create(
    user=inst_user,
    defaults={
        'state': 'IN-DL',
        'institute': 'Dummy Institute 2',
        'department': 'computer engineering',
        'phone_number': '8888888888',
        'position': 'instructor'
    }
)

print("Users created successfully!")
