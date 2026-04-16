import os
import django
from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from workshop_app.models import Profile, Workshop, WorkshopType
import random

# Create Users
def get_or_create_user(username, first, last):
    user, _ = User.objects.get_or_create(username=username)
    user.first_name = first
    user.last_name = last
    user.save()
    return user

wb_user = get_or_create_user('wb_user', 'Coord', 'West Bengal')
pb_user = get_or_create_user('pb_user', 'Coord', 'Punjab')
dl_user = get_or_create_user('dl_user', 'Coord', 'Delhi')
mh_user = get_or_create_user('mh_user', 'Coord', 'Maharashtra')
ka_user = get_or_create_user('ka_user', 'Coord', 'Karnataka')
ap_user = get_or_create_user('ap_user', 'Coord', 'Andhra Pradesh')
instructor = get_or_create_user('inst_user', 'Instructor', '')

# Create Profiles
def create_profile(user, state, institute):
    if not hasattr(user, 'profile'):
        Profile.objects.create(
            user=user, 
            state=state, 
            institute=institute,
            department="computer engineering",
            phone_number="9999999999",
            position="coordinator"
        )

create_profile(wb_user, 'IN-WB', 'Institute In West Bengal')
create_profile(pb_user, 'IN-PB', 'Institute In Punjab')
create_profile(dl_user, 'IN-DL', 'Institute In Delhi')
create_profile(mh_user, 'IN-MH', 'Institute In Maharashtra')
create_profile(ka_user, 'IN-KA', 'Institute In Karnataka')
create_profile(ap_user, 'IN-AP', 'Institute In Andhra')

# Types
wt_scilab, _ = WorkshopType.objects.get_or_create(name='Scilab Scientific Computing', defaults={'description': 'Demo', 'duration': 1, 'terms_and_conditions': 'Demo'})
wt_latex, _ = WorkshopType.objects.get_or_create(name='Latex Typesetting', defaults={'description': 'Demo', 'duration': 1, 'terms_and_conditions': 'Demo'})
wt_django, _ = WorkshopType.objects.get_or_create(name='Advanced Django', defaults={'description': 'Demo', 'duration': 1, 'terms_and_conditions': 'Demo'})
wt_python, _ = WorkshopType.objects.get_or_create(name='Python Basics', defaults={'description': 'Demo', 'duration': 1, 'terms_and_conditions': 'Demo'})
wt_arduino, _ = WorkshopType.objects.get_or_create(name='Arduino Programming', defaults={'description': 'Demo', 'duration': 1, 'terms_and_conditions': 'Demo'})

today = timezone.now().date()

# Delete existing to prevent massive dupes if run repeatedly
Workshop.objects.all().delete()

workshop_scenarios = [
    (wb_user, wt_scilab, today + datetime.timedelta(days=0)),
    (pb_user, wt_latex, today + datetime.timedelta(days=2)),
    (dl_user, wt_django, today + datetime.timedelta(days=5)),
    (mh_user, wt_python, today + datetime.timedelta(days=7)),
    (ka_user, wt_arduino, today + datetime.timedelta(days=10)),
    (ap_user, wt_python, today + datetime.timedelta(days=12)),
    (mh_user, wt_django, today + datetime.timedelta(days=14)),
    (dl_user, wt_scilab, today + datetime.timedelta(days=1)),
    (pb_user, wt_arduino, today + datetime.timedelta(days=3)),
    (ka_user, wt_latex, today + datetime.timedelta(days=8)),
]

for coord, wt, d in workshop_scenarios:
    Workshop.objects.create(
        coordinator=coord,
        instructor=instructor,
        workshop_type=wt,
        date=d,
        status=1,
        tnc_accepted=True
    )

print("Expanded Dummy data seeded successfully!")
