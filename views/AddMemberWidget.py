from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QDateEdit, QComboBox,
    QPushButton, QMessageBox, QLabel, QGridLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
import uuid
from controllers.controller import Controller

class AddMemberWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("הוספת מנוי חדש")
        title_label.setProperty("title", "true")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create a frame for the form with a border
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_frame.setFrameShadow(QFrame.Shadow.Raised)
        
        # Form layout inside the frame
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)
        
        # Set the layout for the frame
        form_frame.setLayout(form_layout)
        
        # Common width for all input fields (50% of total width)
        input_width = 300
        
        # Member number - now read-only and auto-assigned
        self.member_number_input = QLineEdit()
        self.member_number_input.setFixedWidth(input_width)
        self.member_number_input.setReadOnly(True)
        
        # Get the next member number
        next_member_number = Controller.get_highest_member_number() + 1
        self.member_number_input.setText(str(next_member_number))
        self.member_number_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.member_number_input.setStyleSheet("background-color: #444444;")  # Darker background to show it's read-only
        form_layout.addRow("מספר מנוי:", self.member_number_input)
        
        # ID
        self.member_id_input = QLineEdit()
        self.member_id_input.setFixedWidth(input_width)
        self.member_id_input.setPlaceholderText("תעודת זהות")
        self.member_id_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow("ת.ז:", self.member_id_input)
        
        # First name
        self.first_name_input = QLineEdit()
        self.first_name_input.setFixedWidth(input_width)
        self.first_name_input.setPlaceholderText("שם פרטי")
        self.first_name_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow("שם פרטי:", self.first_name_input)
        
        # Last name
        self.last_name_input = QLineEdit()
        self.last_name_input.setFixedWidth(input_width)
        self.last_name_input.setPlaceholderText("שם משפחה")
        self.last_name_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow("שם משפחה:", self.last_name_input)
        
        # Date of birth
        self.dob_input = QDateEdit()
        self.dob_input.setFixedWidth(input_width)
        self.dob_input.setDisplayFormat("dd-MM-yyyy")
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate(1990, 1, 1))  # Default date
        self.dob_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dob_input.setKeyboardTracking(True)  # Enable manual editing
        form_layout.addRow("תאריך לידה:", self.dob_input)
        
        # Gender
        self.gender_input = QComboBox()
        self.gender_input.setFixedWidth(input_width)
        self.gender_input.addItems(["זכר", "נקבה", "אחר"])
        self.gender_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        form_layout.addRow("מגדר:", self.gender_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setFixedWidth(input_width)
        self.email_input.setPlaceholderText("דוא\"ל")
        self.email_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow("דוא\"ל:", self.email_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setFixedWidth(input_width)
        self.phone_input.setPlaceholderText("מספר טלפון")
        self.phone_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow("טלפון:", self.phone_input)
        
        # Address
        self.address_input = QLineEdit()
        self.address_input.setFixedWidth(input_width)
        self.address_input.setPlaceholderText("כתובת מגורים")
        self.address_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow("כתובת:", self.address_input)
        
        # Member type
        self.member_type_input = QComboBox()
        self.member_type_input.setFixedWidth(input_width)
        self.member_type_input.addItems(["רגיל", "VIP", "מוגבל", "סטודנט", "פנסיונר"])
        self.member_type_input.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        form_layout.addRow("סוג מנוי:", self.member_type_input)
        
        # Membership expiry date
        self.membership_exp_input = QDateEdit()
        self.membership_exp_input.setFixedWidth(input_width)
        self.membership_exp_input.setDisplayFormat("dd-MM-yyyy")
        self.membership_exp_input.setCalendarPopup(True)
        self.membership_exp_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.membership_exp_input.setKeyboardTracking(True)  # Enable manual editing
        # Set default expiry to one year from now
        default_exp = QDate.currentDate().addYears(1)
        self.membership_exp_input.setDate(default_exp)
        form_layout.addRow("תפוגת מנוי:", self.membership_exp_input)
        
        # Health declaration expiry date
        self.health_exp_input = QDateEdit()
        self.health_exp_input.setFixedWidth(input_width)
        self.health_exp_input.setDisplayFormat("dd-MM-yyyy")
        self.health_exp_input.setCalendarPopup(True)
        self.health_exp_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.health_exp_input.setKeyboardTracking(True)  # Enable manual editing
        
        # Set default health declaration expiry to six months from now
        default_health_exp = QDate.currentDate().addMonths(6)
        self.health_exp_input.setDate(default_health_exp)
        form_layout.addRow("תפוגת הצהרת בריאות:", self.health_exp_input)
        
        # Add the form frame to the main layout
        main_layout.addWidget(form_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.clear_button = QPushButton("נקה טופס")
        self.clear_button.clicked.connect(self.clear_form)
        self.clear_button.setProperty("secondary", "true")
        button_layout.addWidget(self.clear_button)
        
        self.save_button = QPushButton("שמור מנוי")
        self.save_button.clicked.connect(self.save_member)
        button_layout.addWidget(self.save_button)
        
        main_layout.addSpacing(20)
        main_layout.addLayout(button_layout)
        
        # Set right-to-left layout
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setLayout(main_layout)
    
    def clear_form(self, preserve_member_number=False):
        """Clear all form fields"""
        if not preserve_member_number:
            # Get the next member number
            next_member_number = Controller.get_highest_member_number() + 1
            self.member_number_input.setText(str(next_member_number))
        
        self.member_id_input.clear()
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.dob_input.setDate(QDate(1990, 1, 1))
        self.gender_input.setCurrentIndex(0)
        self.email_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.member_type_input.setCurrentIndex(0)
        
        # Reset expiry dates
        default_exp = QDate.currentDate().addYears(1)
        self.membership_exp_input.setDate(default_exp)
        
        default_health_exp = QDate.currentDate().addMonths(6)
        self.health_exp_input.setDate(default_health_exp)
    
    def save_member(self):
        """Save the member to the database"""
        # Validate required fields
        if not self.member_id_input.text():
            QMessageBox.warning(self, "חסר מידע", "חובה להזין תעודת זהות")
            return
            
        if not self.first_name_input.text() or not self.last_name_input.text():
            QMessageBox.warning(self, "חסר מידע", "חובה להזין שם פרטי ושם משפחה")
            return
        
        # Validate date inputs
        try:
            # Validate date format
            dob = self.dob_input.date().toString("dd-MM-yyyy")
            membership_exp = self.membership_exp_input.date().toString("dd-MM-yyyy")
            healthdec_exp = self.health_exp_input.date().toString("dd-MM-yyyy")
            
            # Additional validation can be added here
        except:
            QMessageBox.warning(self, "שגיאה בתאריך", "אנא הזן תאריכים בפורמט תקין (DD-MM-YYYY)")
            return
            
        # Get the member number from the input field (which is already set to next available number)
        member_number = self.member_number_input.text()
        
        # Double-check that this member number is still available
        if Controller.check_member_number_exists(member_number):
            # If the number was taken while the form was open, get a new number
            member_number = str(Controller.get_highest_member_number() + 1)
            self.member_number_input.setText(member_number)
        
        # Prepare the member data
        member_data = {
            "member_number": member_number,
            "member_id": self.member_id_input.text(),
            "first_name": self.first_name_input.text(),
            "last_name": self.last_name_input.text(),
            "date_of_birth": dob,
            "gender": self.gender_input.currentText(),
            "email": self.email_input.text(),
            "phone_number": self.phone_input.text(),
            "home_address": self.address_input.text(),
            "member_type": self.member_type_input.currentText(),
            "first_created": datetime.now().strftime("%d-%m-%Y"),
            "membership_exp_date": membership_exp,
            "healthdec_exp_date": healthdec_exp,
            "member_uuid": str(uuid.uuid4()),
            "last_visits": []
        }
        
        try:
            # Save the member
            result = Controller.create_new_member(member_data)
            if result:
                QMessageBox.information(self, "הצלחה", f"המנוי {self.first_name_input.text()} {self.last_name_input.text()} נוסף בהצלחה!")
                
                # After successful save, update the member number for the next member
                next_member_number = Controller.get_highest_member_number() + 1
                self.member_number_input.setText(str(next_member_number))
                
                # Clear the rest of the form
                self.clear_form(preserve_member_number=True)
            else:
                QMessageBox.warning(self, "שגיאה", "אירעה שגיאה בשמירת המנוי")
        except Exception as e:
            QMessageBox.critical(self, "שגיאה", f"אירעה שגיאה: {str(e)}") 