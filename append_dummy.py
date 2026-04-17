import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django Environment (for standalone running, though we'll use shell)
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workshop_booking.settings')
    django.setup()

from django.contrib.auth.models import User, Group
from workshop_app.models import Workshop, WorkshopType, Profile
from teams.models import Team

print("Appending 30 dummy workshop records...")

# Get main test users
coord_user, _ = User.objects.get_or_create(username='coordinator')
inst_user, _ = User.objects.get_or_create(username='instructor')

# Ensure they have profiles
def ensure_profile(user, position):
    if not hasattr(user, 'profile'):
        Profile.objects.create(
            user=user,
            phone_number="9876543210",
            institute="Demo Institute IT",
            department="Computer Science",
            position=position,
            location="Demo City",
            state="IN-MH"
        )
    # Ensure they are verified so they don't hit the activation page
    user.profile.is_email_verified = True
    user.profile.save()

ensure_profile(coord_user, 'coordinator')
ensure_profile(inst_user, 'instructor')

# Add to groups
coord_group, _ = Group.objects.get_or_create(name='coordinator')
inst_group, _ = Group.objects.get_or_create(name='instructor')
coord_user.groups.add(coord_group)
inst_user.groups.add(inst_group)

types = list(WorkshopType.objects.all())
if not types:
    wt, _ = WorkshopType.objects.get_or_create(name="Web Development with Python", defaults={'duration': 2, 'description': 'Learn Django and Flask'})
    types = [wt]

statuses = [0, 1, 2] 
today = timezone.now().date()

# Get an admin
admin_user = User.objects.filter(is_superuser=True).first()

for i in range(30):
    # Alternate owners between coordinator and admin
    owner = coord_user if i % 2 == 0 else admin_user
    assigned_inst = inst_user if i % 3 != 0 else None 
    
    status = random.choice(statuses)
    if status == 1: 
        assigned_inst = inst_user
        
    Workshop.objects.create(
        coordinator=owner,
        instructor=assigned_inst,
        workshop_type=random.choice(types),
        date=today + timedelta(days=random.randint(-30, 60)),
        status=status,
        tnc_accepted=True
    )

    # Ensure a team exists for team stats to work
    if not Team.objects.exists():
        print("Creating a demo team...")
        team = Team.objects.create(creator=admin_user)
        # Add instructor to the team members
        if hasattr(inst_user, 'profile'):
            team.members.add(inst_user.profile)
    else:
        # Add instructor to first team if not there
        team = Team.objects.first()
        if hasattr(inst_user, 'profile'):
            team.members.add(inst_user.profile)

print("Successfully appended 30 workshop records!")
