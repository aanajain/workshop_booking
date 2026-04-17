import random
import datetime
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workshop_portal.settings')
django.setup()

from django.contrib.auth.models import User
from workshop_app.models import Workshop, WorkshopType, Profile
from django.utils import timezone

def generate_data():
    print("Clearing existing workshops...")
    Workshop.objects.all().delete()
    
    users = list(User.objects.all())
    types = list(WorkshopType.objects.all())
    states_list = ['IN-MH', 'IN-DL', 'IN-KA', 'IN-TN', 'IN-GJ', 'IN-UP', 'IN-WB']
    
    if not types:
        print("No WorkshopTypes found. Please create them first.")
        return

    print("Generating 30 workshops...")
    for i in range(30):
        coord = random.choice(users)
        instr = random.choice(users)
        w_type = random.choice(types)
        
        # Ensure coordinator has a profile
        if not hasattr(coord, 'profile'):
            Profile.objects.create(
                user=coord,
                institute="Test Institute",
                department="computer engineering",
                phone_number="9999999999",
                position="coordinator",
                state=random.choice(states_list)
            )
        else:
            coord.profile.state = random.choice(states_list)
            coord.profile.save()
            
        # Random date between -60 and +60 days from today
        days_offset = random.randint(-60, 60)
        ws_date = timezone.now().date() + datetime.timedelta(days=days_offset)
        
        # Create workshop with status=1 (Accepted/Success)
        ws = Workshop.objects.create(
            coordinator=coord,
            instructor=instr,
            workshop_type=w_type,
            date=ws_date,
            status=1,
            tnc_accepted=True
        )
        
        print(f"[{i+1}/30] Created: {w_type.name} on {ws_date} (State: {coord.profile.state})")

if __name__ == "__main__":
    generate_data()
    print("Done!")
