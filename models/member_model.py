from datetime import datetime, date
import uuid

class Member:
    def __init__(
        self,
        member_number, first_name, last_name, date_of_birth, gender, email, phone_number, home_address,
        member_type, first_created, membership_exp_date, healthdec_exp_date,
        member_uuid=None, member_id=None, last_visits=None, member_status=None
    ):
        self.member_uuid = member_uuid if member_uuid else str(uuid.uuid4())
        self.member_id = member_id
        self.member_number = member_number
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.phone_number = phone_number
        self.home_address = home_address
        self.member_type = member_type
        self.first_created = first_created
        self.membership_exp_date = membership_exp_date
        self.healthdec_exp_date = healthdec_exp_date
        self.last_visits = last_visits if last_visits else []
        self.member_status = member_status
        self.update_status()

    def update_status(self):
        if self.check_member_expiry():
            self.member_status = "Inactive"
        elif self.check_member_healthdec_expiry():
            self.member_status = "Inactive"
        else:
            self.member_status = "Active"

    def check_member_expiry(self):
        current_date = datetime.today()
        expiry_date = datetime.strptime(self.membership_exp_date, "%d-%m-%Y")
        return current_date > expiry_date

    def check_member_healthdec_expiry(self):
        current_date = date.today()
        expiry_date = datetime.strptime(self.healthdec_exp_date, "%d-%m-%Y").date()
        return current_date > expiry_date

    def to_dict(self):
        return {
            "member_uuid": self.member_uuid,
            "member_id": self.member_id,
            "member_number": self.member_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "email": self.email,
            "phone_number": self.phone_number,
            "home_address": self.home_address,
            "member_type": self.member_type,
            "first_created": self.first_created,
            "membership_exp_date": self.membership_exp_date,
            "healthdec_exp_date": self.healthdec_exp_date,
            "last_visits": self.last_visits,
            "member_status": self.member_status
        }

    def __str__(self):
        return f"Member(id={self.member_id}, name={self.first_name} {self.last_name}, email={self.email}, phone={self.phone_number})"
