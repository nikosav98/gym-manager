from models.db_model import (
    get_all_members, 
    get_member_count, 
    fetch_member_by_id,
    fetch_member_by_number,
    create_member, 
    update_member,
    delete_member,
    check_member_number_exists
)
import hashlib

class Controller:
    @staticmethod
    def get_member_list_data(offset=0, limit=20):
        """Get a page of member data for display in the list view"""
        members = get_all_members(offset, limit)
        return [member.to_dict() for member in members]
    
    @staticmethod
    def get_member_count():
        """Get the total count of members in the database"""
        return get_member_count()
    
    @staticmethod
    def get_member_by_id(member_id):
        """Get a specific member by their ID"""
        member = fetch_member_by_id(member_id)
        if member:
            return member.to_dict()
        return None
    
    @staticmethod
    def create_new_member(member_data):
        """Create a new member from the given data"""
        # The member_data dictionary should contain all required fields
        from models.member_model import Member
        member = Member(
            member_number=member_data.get("member_number"),
            first_name=member_data.get("first_name"),
            last_name=member_data.get("last_name"),
            date_of_birth=member_data.get("date_of_birth"),
            gender=member_data.get("gender"),
            email=member_data.get("email"),
            phone_number=member_data.get("phone_number"),
            home_address=member_data.get("home_address"),
            member_type=member_data.get("member_type"),
            first_created=member_data.get("first_created"),
            membership_exp_date=member_data.get("membership_exp_date"),
            healthdec_exp_date=member_data.get("healthdec_exp_date"),
            member_uuid=member_data.get("member_uuid"),
            member_id=member_data.get("member_id"),
            last_visits=member_data.get("last_visits", []),
            member_status=member_data.get("member_status")
        )
        create_member(member)
        return member.to_dict()
    
    @staticmethod
    def update_existing_member(member_data):
        """Update an existing member with the given data"""
        # The member_data dictionary should contain the member_id and updated fields
        from models.member_model import Member
        
        # First fetch the current member to ensure we have all data
        current_member = fetch_member_by_id(member_data.get("member_id"))
        if not current_member:
            return None
        
        # Update the member with the new data
        for key, value in member_data.items():
            setattr(current_member, key, value)
        
        # Save the updated member
        update_member(current_member)
        return current_member.to_dict()
    
    @staticmethod
    def delete_member(member_id):
        """Delete a member by their ID"""
        delete_member(member_id)
        return True
        
    @staticmethod
    def add_member_attendace_and_return_data(member_number):
        """Record member attendance and return member data for display"""
        try:
            # Get the member by their member number
            member = fetch_member_by_number(member_number)
            
            if member:
                # Found the member, update their attendance
                from datetime import datetime
                today = datetime.now().strftime("%d-%m-%Y")
                today_time = datetime.now().strftime("%H:%M")
                
                # Add today's date and time to last_visits
                if not hasattr(member, 'last_visits') or member.last_visits is None:
                    member.last_visits = []
                
                visit_record = f"{today} {today_time}"
                member.last_visits.append(visit_record)
                
                # Update member in database
                update_member(member)
                
                # Return the member data as a dictionary
                return member.to_dict()
            
            # If we got here, no member was found with that number
            return None
            
        except Exception as e:
            print(f"Error in add_member_attendace_and_return_data: {e}")
            return None
            
    @staticmethod
    def validate_admin_login(username, password_hash):
        """Validate admin login credentials"""
        # For demo purposes, using hardcoded credentials
        # In a real application, this would check against a database
        admin_username = "admin"
        admin_password = "123"
        expected_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        # Log the login attempt
        with open("action_log.txt", "a") as log_file:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if username == admin_username and password_hash == expected_hash:
                log_file.write(f"{timestamp} - INFO - Successful admin login\n")
                return True
            else:
                if username == admin_username:
                    log_file.write(f"{timestamp} - WARNING - Failed login attempt with correct username\n")
                else:
                    log_file.write(f"{timestamp} - WARNING - Failed login attempt with username: {username}\n")
                return False

    @staticmethod
    def check_member_number_exists(member_number):
        """
        Check if a member number already exists in the database
        Returns True if the member number exists, False otherwise
        """
        from models.db_model import check_member_number_exists as db_check_member_number
        return db_check_member_number(member_number)

    @staticmethod
    def get_highest_member_number():
        """Get the highest member number currently in the database"""
        from models.db_model import get_highest_member_number
        return get_highest_member_number()
