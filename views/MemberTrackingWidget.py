from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QComboBox, QHBoxLayout, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from controllers.controller import Controller

import timeit#debug

class MemberTrackingWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent_window = parent  # Store reference to MainWindow

        # Main layout for the widget
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Create a frame for the search section
        search_frame = QFrame()
        search_frame.setFrameShape(QFrame.Shape.StyledPanel)
        search_frame.setFrameShadow(QFrame.Shadow.Raised)
        
        search_layout = QGridLayout(search_frame)
        search_layout.setVerticalSpacing(10)
        search_layout.setHorizontalSpacing(10)
        search_layout.setContentsMargins(15, 15, 15, 15)

        # Input field and confirm button layout
        self.member_input = QLineEdit(self)
        self.member_input.setPlaceholderText("הקלד מספר מנוי")
        self.member_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.member_input.setStyleSheet("font-size: 18px;")
        
        self.confirm_button = QPushButton("אישור", self)
        self.confirm_button.clicked.connect(self.toggle_member_display)
        
        # Add to search layout
        search_layout.addWidget(self.member_input, 0, 0, 1, 3)
        search_layout.addWidget(self.confirm_button, 0, 3, 1, 1)
        
        # Create a frame for displaying member details
        display_frame = QFrame()
        display_frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        display_layout = QVBoxLayout(display_frame)
        display_layout.setSpacing(15)
        display_layout.setContentsMargins(15, 15, 15, 15)

        # Label container for member details
        self.member_details_label = QLabel("", self)
        self.member_details_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.member_details_label.setStyleSheet("font-size: 18px;")
        self.member_details_label.setWordWrap(True)
        display_layout.addWidget(self.member_details_label)

        # Status label for member status (Active/Inactive)
        self.member_status_label = QLabel("", self)
        self.member_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.member_status_label.setStyleSheet("font-size: 24px;")
        display_layout.addWidget(self.member_status_label)
        
        # Controls layout
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Clear button
        self.clear_button = QPushButton("נקה", self)
        self.clear_button.clicked.connect(self.clear_display)
        self.clear_button.setProperty("secondary", "true")
        
        # Timeout dropdown
        timeout_label = QLabel("משך תצוגה:")
        timeout_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.timeout_dropdown = QComboBox(self)
        self.timeout_dropdown.addItems(["Never", "2 seconds", "5 seconds", "10 seconds"])
        self.timeout_dropdown.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        controls_layout.addWidget(self.clear_button)
        controls_layout.addStretch()
        controls_layout.addWidget(timeout_label)
        controls_layout.addWidget(self.timeout_dropdown)
        
        display_layout.addLayout(controls_layout)

        # Add frames to main layout
        self.layout.addWidget(search_frame)
        self.layout.addWidget(display_frame, 1)  # Give the display frame more space
        
        # Set the layout for the widget
        self.setLayout(self.layout)

        # Connect Enter key to trigger the confirm button click
        self.member_input.returnPressed.connect(self.toggle_member_display)
        
        # Set right-to-left layout direction
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Timer for clearing the label
        self.clear_timer = QTimer(self)
        self.clear_timer.timeout.connect(self.clear_display)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):  # Check for Enter or Return key
            self.confirm_button.click()  # Emulate button click
        else:
            super().keyPressEvent(event)  # Pass other key events to the parent

    def toggle_member_display(self):
        """
        Toggles between showing member details and clearing the displayed information.
        """
        # Get the input member number
        member_number = self.member_input.text().strip()

        if member_number:  # Proceed only if the input is not empty
            # Fetch the (safe) member data from the controller
            start = timeit.default_timer()#debug
            info_to_display = Controller.add_member_attendace_and_return_data(member_number)
            if info_to_display:
                # Display member details
                self.display_member_details(info_to_display)
            else:
                # Show error if member not found
                self.member_details_label.setText("מנוי לא נמצא. אנא הזן מספר מנוי תקין.")
                self.member_status_label.clear()  # Clear status label in case of error
        else:
            # Show error for empty input
            self.member_details_label.setText("אנא הזן מספר מנוי.")
            self.member_status_label.clear()  # Clear status label in case of empty input

        self.start_clear_timer()

        stop = timeit.default_timer()#debug
        print('Time: ', stop - start) #debug

    def display_member_details(self, info_to_display):
        """
        Displays the required details of the member.
        """
        # Format the membership expiry date to highlight if close to expiry
        membership_exp = info_to_display.get('membership_exp_date', '')
        healthdec_exp = info_to_display.get('healthdec_exp_date', '')
        
        # Format a complete member profile
        self.member_details_label.setText(
            f"<b>שם:</b> {info_to_display.get('first_name', '')} {info_to_display.get('last_name', '')}<br>"
            f"<b>מספר מנוי:</b> {info_to_display.get('member_number', '')}<br>"
            f"<b>ת.ז:</b> {info_to_display.get('member_id', '')}<br>"
            f"<b>אימייל:</b> {info_to_display.get('email', '')}<br>"
            f"<b>טלפון:</b> {info_to_display.get('phone_number', '')}<br>"
            f"<b>כתובת:</b> {info_to_display.get('home_address', '')}<br>"
            f"<b>סוג מנוי:</b> {info_to_display.get('member_type', '')}<br>"
            f"<b>תאריך הצטרפות:</b> {info_to_display.get('first_created', '')}<br>"
            f"<b>תפוגת מנוי:</b> {membership_exp}<br>"
            f"<b>תפוגת הצהרת בריאות:</b> {healthdec_exp}<br>"
            f"<b>ביקור אחרון:</b> {info_to_display.get('last_visits', [''])[-1] if info_to_display.get('last_visits') else ''}"
        )
        
        # Set member status and change color based on status
        member_status = info_to_display['member_status']
        status_text = "פעיל" if member_status == "Active" else "לא פעיל"
        self.member_status_label.setText(f"סטטוס: {status_text}")
        
        if member_status == "Active":
            self.member_status_label.setProperty("status", "active")
            self.member_status_label.setStyleSheet("font-size: 24px;")
        elif member_status == "Inactive":
            self.member_status_label.setProperty("status", "inactive")
            self.member_status_label.setStyleSheet("font-size: 24px;")
        else:
            self.member_status_label.setProperty("status", "")
            self.member_status_label.setStyleSheet("font-size: 24px; color: black; font-weight: bold;")
        
        # Force style refresh
        self.member_status_label.style().unpolish(self.member_status_label)
        self.member_status_label.style().polish(self.member_status_label)
        
        self.member_input.clear()
        self.start_clear_timer()

    def clear_display(self): 
        """Clears the member details and input field."""
        self.member_details_label.clear()
        self.member_status_label.clear()  # Clear the status label as well
        self.member_input.clear()
        self.clear_timer.stop()  # Stop the timer when manually cleared

    def start_clear_timer(self): 
        """Starts the timer for clearing the member details based on the selected timeout."""
        timeout_text = self.timeout_dropdown.currentText()
        if timeout_text == "Never":
            self.clear_timer.stop()
        else:
            timeout_seconds = int(timeout_text.split()[0])
            self.clear_timer.start(timeout_seconds * 1000)
