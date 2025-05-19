import random
import uuid
import string
from datetime import datetime, timedelta
import os
import sys

# Add the project root to the path to import the models
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from models.member_model import Member
from models.db_model import create_member, init_db

def generate_random_string(length=8):
    """Generate a random string of specified length"""
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_random_id():
    """Generate a random ID number (9 digits)"""
    return ''.join(random.choices(string.digits, k=9))

def generate_random_phone():
    """Generate a random phone number"""
    return f"05{random.randint(0, 9)}-{random.randint(1000000, 9999999)}"

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date"""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def format_date(date_obj):
    """Format a date object as DD-MM-YYYY"""
    return date_obj.strftime("%d-%m-%Y")

def populate_database(num_members=10):
    """Populate the database with random members"""
    # Ensure the database is initialized
    init_db()
    
    # Names for random generation
    first_names = ["לירון", "עומר", "שרון", "טל", "עידן", "הדר", "רון", "דנה", "יעל", "אלון"]
    last_names = ["כהן", "לוי", "מזרחי", "אברהם", "פרץ", "אזולאי", "דהן", "אוחנה", "ביטון", "גבאי"]
    member_types = ["רגיל", "VIP", "מוגבל", "סטודנט", "פנסיונר"]
    genders = ["זכר", "נקבה"]
    
    # Time references
    now = datetime.now()
    one_year_ago = now - timedelta(days=365)
    two_years_future = now + timedelta(days=365*2)
    
    # Create members
    for i in range(num_members):
        # Generate basic member data
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        gender = random.choice(genders)
        member_type = random.choice(member_types)
        member_id = generate_random_id()
        
        # Generate dates
        dob = generate_random_date(datetime(1970, 1, 1), datetime(2000, 12, 31))
        first_created = format_date(generate_random_date(one_year_ago, now))
        
        # Set expiry dates - some active, some expired for testing
        if random.choice([True, False, False]):  # 1/3 chance of expired membership
            membership_exp_date = format_date(generate_random_date(one_year_ago, now))
        else:
            membership_exp_date = format_date(generate_random_date(now, two_years_future))
            
        if random.choice([True, False, False]):  # 1/3 chance of expired health declaration
            healthdec_exp_date = format_date(generate_random_date(one_year_ago, now))
        else:
            healthdec_exp_date = format_date(generate_random_date(now, two_years_future))
        
        # Create a Member object
        member = Member(
            member_number=i,  # Sequential numbers starting from 0
            first_name=first_name,
            last_name=last_name,
            date_of_birth=format_date(dob),
            gender=gender,
            email=f"{first_name.lower()}.{last_name.lower()}@example.com",
            phone_number=generate_random_phone(),
            home_address=f"רחוב {generate_random_string(6)} {random.randint(1, 100)}, {random.choice(['תל אביב', 'ירושלים', 'חיפה', 'באר שבע', 'אילת'])}",
            member_type=member_type,
            first_created=first_created,
            membership_exp_date=membership_exp_date,
            healthdec_exp_date=healthdec_exp_date,
            member_uuid=str(uuid.uuid4()),
            member_id=member_id,
            last_visits=[],
            member_status=None  # Will be set by the Member constructor's update_status method
        )
        
        # Add to database
        create_member(member)
        print(f"Created member: {member.first_name} {member.last_name} (ID: {member.member_id}, Number: {member.member_number})")
    
    print(f"\nSuccessfully added {num_members} members to the database.")

if __name__ == "__main__":
    populate_database() 