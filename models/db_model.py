import sqlite3
from datetime import datetime, date
import os
import uuid
import sys
import os

# Adjust import path to find member_model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.member_model import Member

# Use a relative path that works from any working directory
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "gym_database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the 'members' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_uuid TEXT NOT NULL,
            member_id TEXT NOT NULL,
            member_number INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            gender TEXT NOT NULL,
            email TEXT,
            phone_number TEXT,
            home_address TEXT,
            member_type TEXT NOT NULL,
            first_created TEXT NOT NULL,
            membership_exp_date TEXT NOT NULL,
            healthdec_exp_date TEXT NOT NULL,
            last_visits TEXT,
            member_status TEXT NOT NULL
        )
    ''')
    
    # Create an index on member_id for faster lookups
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_member_id ON members(member_id)')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def create_member(member):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO members (
            member_uuid, member_id, member_number, first_name, last_name, 
            date_of_birth, gender, email, phone_number, home_address, 
            member_type, first_created, membership_exp_date, healthdec_exp_date, 
            last_visits, member_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        member.member_uuid, member.member_id, member.member_number, member.first_name, member.last_name, 
        member.date_of_birth, member.gender, member.email, member.phone_number, member.home_address, 
        member.member_type, member.first_created, member.membership_exp_date, member.healthdec_exp_date, 
        str(member.last_visits), member.member_status
    ))
    conn.commit()
    conn.close()

def update_member(member):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE members SET 
            first_name=?, last_name=?, date_of_birth=?, gender=?, email=?, 
            phone_number=?, home_address=?, member_type=?, 
            membership_exp_date=?, healthdec_exp_date=?, 
            last_visits=?, member_status=? 
        WHERE member_id=?
    ''', (
        member.first_name, member.last_name, member.date_of_birth, member.gender, member.email, 
        member.phone_number, member.home_address, member.member_type, 
        member.membership_exp_date, member.healthdec_exp_date, 
        str(member.last_visits), member.member_status, member.member_id
    ))
    conn.commit()
    conn.close()

# Admin level operation
def delete_member(member_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM members WHERE member_id=?', (member_id,))
    conn.commit()
    conn.close()

def fetch_member_by_id(member_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members WHERE member_id=?', (member_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        # Map database columns to Member constructor parameters
        # [id, member_uuid, member_id, member_number, first_name, last_name, date_of_birth, gender, 
        # email, phone_number, home_address, member_type, first_created, membership_exp_date, 
        # healthdec_exp_date, last_visits, member_status]
        
        # Extract fields and convert to the format Member expects
        member_number = result[3]
        first_name = result[4]
        last_name = result[5]
        date_of_birth = result[6]
        gender = result[7]
        email = result[8]
        phone_number = result[9]
        home_address = result[10]
        member_type = result[11]
        first_created = result[12]
        membership_exp_date = result[13]
        healthdec_exp_date = result[14]
        member_uuid = result[1]
        member_id = result[2]
        last_visits = eval(result[15]) if result[15] else []
        member_status = result[16]
        
        return Member(
            member_number=member_number, 
            first_name=first_name, 
            last_name=last_name,
            date_of_birth=date_of_birth, 
            gender=gender, 
            email=email, 
            phone_number=phone_number,
            home_address=home_address, 
            member_type=member_type, 
            first_created=first_created,
            membership_exp_date=membership_exp_date, 
            healthdec_exp_date=healthdec_exp_date,
            member_uuid=member_uuid, 
            member_id=member_id, 
            last_visits=last_visits,
            member_status=member_status
        )
    return None

def get_all_members(offset=0, limit=20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members ORDER BY member_number DESC LIMIT ? OFFSET ?', (limit, offset))
    results = cursor.fetchall()
    conn.close()
    
    members = []
    for result in results:
        # Same mapping as in fetch_member_by_id
        member_number = result[3]
        first_name = result[4]
        last_name = result[5]
        date_of_birth = result[6]
        gender = result[7]
        email = result[8]
        phone_number = result[9]
        home_address = result[10]
        member_type = result[11]
        first_created = result[12]
        membership_exp_date = result[13]
        healthdec_exp_date = result[14]
        member_uuid = result[1]
        member_id = result[2]
        last_visits = eval(result[15]) if result[15] else []
        member_status = result[16]
        
        member = Member(
            member_number=member_number, 
            first_name=first_name, 
            last_name=last_name,
            date_of_birth=date_of_birth, 
            gender=gender, 
            email=email, 
            phone_number=phone_number,
            home_address=home_address, 
            member_type=member_type, 
            first_created=first_created,
            membership_exp_date=membership_exp_date, 
            healthdec_exp_date=healthdec_exp_date,
            member_uuid=member_uuid, 
            member_id=member_id, 
            last_visits=last_visits,
            member_status=member_status
        )
        members.append(member)
    
    return members

def get_member_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM members')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def fetch_member_by_number(member_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members WHERE member_number=?', (member_number,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        # Map database columns to Member constructor parameters just like in fetch_member_by_id
        member_number = result[3]
        first_name = result[4]
        last_name = result[5]
        date_of_birth = result[6]
        gender = result[7]
        email = result[8]
        phone_number = result[9]
        home_address = result[10]
        member_type = result[11]
        first_created = result[12]
        membership_exp_date = result[13]
        healthdec_exp_date = result[14]
        member_uuid = result[1]
        member_id = result[2]
        last_visits = eval(result[15]) if result[15] else []
        member_status = result[16]
        
        return Member(
            member_number=member_number, 
            first_name=first_name, 
            last_name=last_name,
            date_of_birth=date_of_birth, 
            gender=gender, 
            email=email, 
            phone_number=phone_number,
            home_address=home_address, 
            member_type=member_type, 
            first_created=first_created,
            membership_exp_date=membership_exp_date, 
            healthdec_exp_date=healthdec_exp_date,
            member_uuid=member_uuid, 
            member_id=member_id, 
            last_visits=last_visits,
            member_status=member_status
        )
    return None

def check_member_number_exists(member_number):
    """
    Check if a member number already exists in the database
    Returns True if the member number exists, False otherwise
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM members WHERE member_number=?', (member_number,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def get_highest_member_number():
    """
    Get the highest member number currently in the database
    Returns 0 if no members exist
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(member_number) FROM members')
    result = cursor.fetchone()[0]
    conn.close()
    return result if result is not None else 0

# Initialize the database
init_db()
