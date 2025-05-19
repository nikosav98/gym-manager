import threading
import logging
import sqlite3
import uuid
from datetime import date, datetime
from jsonpath_ng import parse

DB_FILE = "../data/gym_database.db"
LOG_FILE = "action_log.txt"

import timeit #debug


db_lock = threading.Lock() # a single lock for database access

#Initial logger setup with configuration
def setup_logger():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO, #Default level
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
        datefmt="%Y-%m-%d %H:%M:%S",  # Timestamp format
    )
    #''' CONSOLE LOGGING - DEBUG
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
    logging.getLogger().addHandler(console_handler)
    #'''
    
#PRESET
#Log action with certain level
def log_action(action, level):
    """
    Log an action with a timestamp.
    :param action: Description of the action performed.
    :param level: Log level (INFO, WARNING, ERROR, etc.)
    """
    if level == "INFO":
        logging.info(action)
    elif level == "WARNING":
        logging.warning(action)
    elif level == "ERROR":
        logging.error(action)
    else:
        logging.debug(action)

# Initialize database
def initialize_database():
    with db_lock, sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Create members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT NOT NULL,
                member_id TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                date_of_birth TEXT,
                gender TEXT,
                email TEXT,
                phone_number TEXT,
                home_address TEXT,
                member_type TEXT,
                first_created TEXT,
                membership_exp_date TEXT,
                healthdec_exp_date TEXT,
                member_status TEXT
            )
        """)
        conn.commit()
    log_action("Database initialized", "INFO")

# returns total counnt of members in database
def get_total_members_count():
    with db_lock, sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM members")
        count = cursor.fetchone()[0]  # Fetch the result and get the count from the tuple
    return count

def update_member_status(member_id):
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d') 

    with sqlite3.connect('your_database.db') as conn:
        cursor = conn.cursor()
        
        # Retrieve the expiration date of the user
        cursor.execute("SELECT expiration_date, status FROM users WHERE user_id = ?", (member_id,))
        user = cursor.fetchone()

        if not user:
            print(f"User with ID {user_id} not found.")
            return None
        
        expiration_date, current_status = user
        
        # Compare today's date with the expiration date
        if today < expiration_date:
            new_status = 'active'  # User is still valid
        elif today == expiration_date:
            new_status = 'inactive'  # User's expiration date has passed today
        else:
            new_status = 'frozen'  # User is inactive after the expiration date

# Function to add a new member to databse (i.e registration)
# Add a new member
def add_new_member(member_id, first_name, last_name, date_of_birth, gender, email, phone_number, home_address, member_type, membership_exp_date, healthdec_exp_date):
    member_uuid = str(uuid.uuid4())
    first_created = datetime.now().strftime("%d%m%Y")
    member_status = update_member_status(member_id) # Set initial status
    with db_lock, sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO members (
                uuid, member_id, first_name, last_name, date_of_birth,
                gender, email, phone_number, home_address, member_type,
                first_created, membership_exp_date, healthdec_exp_date, member_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            member_uuid, member_id, first_name, last_name, date_of_birth,
            gender, email, phone_number, home_address, member_type,
            first_created, membership_exp_date, healthdec_exp_date, member_status
        ))
        conn.commit()
    log_action(f"New member added: {first_name} {last_name}", "INFO")

# Get the member count
def get_member_count():
    with db_lock, sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM members")
        count = cursor.fetchone()[0]
    return count

# Fetch member by ID
def get_member_by_id(member_id):
    with db_lock, sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
        member = cursor.fetchone()
    if member:
        return member
    else:
        log_action(f"No member found with ID {member_id}", "WARNING")
        return None
    
def track_attendance(member_id):
    with db_lock, sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # Check if the member exists
        member = get_member_by_id(member_id)
        if not member:
            return f"Member ID {member_id} not found."

        # Insert or update attendance
        cursor.execute(
            """
            INSERT INTO attendance (member_id, attendance_date)
            VALUES (?, DATE('now'))
            ON CONFLICT(member_id, attendance_date) DO UPDATE SET
            last_updated = CURRENT_TIMESTAMP
            """,
            (member_id,)
        )
        conn.commit()
        return f"Attendance tracked for member ID {member_id}."

def log_action(message, level="INFO"):
    print(f"[{level}] {message}")

''' 
#Function to track member attandance. Recieves a member class
def attandance_tracker(member_class):
    today = date.today().strftime("%d/%m/%Y")
    current_time = datetime.now().strftime("%H:%M")
    
    if member_class.add_attendance(today, current_time):
        # Update the database with the modified member
        data = load_database()
        for member in data["members"]:
            if member["member_number"] == member_class.member_number:
                full_name = member_class.first_name + " " + member_class.last_name
                member.update(member_class.to_dict())
                log_action(f"Attendance logged for member {full_name} ({member_class.member_number}) at current time", level="INFO")
                break
        update_database(DATABASE_FILE, data)
    else:
        log_action(f"Member {member_class.first_name} ({member_class.member_number}) has already attended today", level="INFO")





# Return only non-sensetive data
# Used by MemberTrackingWidget
def get_member_safe_data_by_number(member_number):
    member_class = get_member_by_number(member_number) # get member class instance
    if member_class:
        attandance_tracker(member_class) # update the attandance
        #Return safe data
        safe_data = {
            "first_name": member_class.first_name,
            "last_name": member_class.last_name,
            "member_number": member_class.member_number,
            "member_status": member_class.member_status
        }
        return safe_data
    else:
        return False

# Function to update member information based on field and new value
# FIELD AND NEW VALUE MUST BE CHECKED IN CONTROLLER TODO
def update_member_info(member_number, field, new_value):
    member_class = get_member_by_number(member_number)
    if not member_class:
        log_action(f"Member with number {member_number} not found", level="ERROR")
        return
    
    # Name before update
    previous_name = member_class.first_name + " " + member_class.last_name
    # Update the member's field using the update_info method
    if member_class.update_info(field, new_value):
        # Load the existing data and update the member's info
        data = load_database()
        for member in data["members"]:
            if member["member_number"] == member_number:
                member.update(member_class.to_dict())  # Update the dictionary with the updated member info
                log_action(f"Member {previous_name} ({member_class.member_number}) info updated: {field} = {new_value}", level="INFO")
                break
        
        # Save the updated database
        update_database(DATABASE_FILE, data)
    else:
        log_action(f"Failed to update member {member_class.first_name} ({member_class.member_number}) info for field: {field}", level="ERROR")

def get_member_list_data(start_index, end_index): # Returns  members dict from start i to end i
    data = load_database() 
    members = data["members"]  
    return members[start_index:end_index] 
'''  


def main():
    setup_logger()
    start = timeit.default_timer() #debug
    initialize_database() # INIT DB
    stop = timeit.default_timer() #debug
    
    print('DB Init time: ', stop - start) #debug
    
    # Example actions
    
    for i in range(1,11):
        member_id = 0 + i
        add_new_member(member_id, "first_name", "last_name", "01012020", "Male", "google@braude.ac.il", "050123456","baz 51", "student", "01012027", "20202050" )
    start = timeit.default_timer()
    get_member_by_id(1999)
    stop = timeit.default_timer()
    print('get my member by id time: ', stop - start)  
    #print(f"Member count: {get_member_count()}")
    #print(get_member_by_id("123456"))

if __name__ == "__main__":
    main()