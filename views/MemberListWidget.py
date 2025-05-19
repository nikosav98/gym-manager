from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QHBoxLayout,
    QHeaderView, QComboBox, QApplication, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from controllers.controller import Controller

class MemberListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_page = 0
        self.items_per_page = 20
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Filter section frame
        filter_frame = QFrame()
        filter_frame.setFrameShape(QFrame.Shape.StyledPanel)
        filter_frame.setFrameShadow(QFrame.Shadow.Raised)
        
        # Filter layout
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)

        # Add a label indicating sorting order
        sort_label = QLabel("מיון: מנויים חדשים תחילה")
        filter_layout.addWidget(sort_label)
        
        filter_layout.addStretch()

        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems([ 
            "מספר מנוי", "ת.ז", "סטטוס", "שם פרטי", "שם משפחה"
        ])
        filter_layout.addWidget(self.filter_dropdown)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("ערך לסינון")
        self.filter_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.filter_input.textChanged.connect(self.on_filter_text_changed)
        filter_layout.addWidget(self.filter_input)

        self.apply_filter_button = QPushButton("סנן")
        self.apply_filter_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(self.apply_filter_button)

        layout.addWidget(filter_frame)

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "מספר מנוי", "ת.ז", "סטטוס", "שם פרטי", "שם משפחה", "תפוגת מנוי", "תפוגת אישור בריאות"
        ])
        self.table.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        # Pagination buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.previous_button = QPushButton("הקודם")
        self.previous_button.setFixedWidth(80)
        self.previous_button.setProperty("secondary", "true")
        self.previous_button.clicked.connect(self.previous_page)
        button_layout.addWidget(self.previous_button)

        self.next_button = QPushButton("הבא")
        self.next_button.setFixedWidth(80)
        self.next_button.setProperty("secondary", "true")
        self.next_button.clicked.connect(self.next_page)
        button_layout.addWidget(self.next_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Set up instance variables for filtering
        self.filter_text = ""
        self.filter_field = "member_number"  # Default filter field
        self.filter_dropdown.currentIndexChanged.connect(self.on_filter_field_changed)
        
        self.populate_table()  # Initial data load
        
    def on_filter_field_changed(self, index):
        """Update the filter field when dropdown selection changes"""
        filter_fields = ["member_number", "member_id", "member_status", "first_name", "last_name"]
        self.filter_field = filter_fields[index]
        # Apply filter immediately if there's filter text
        if self.filter_text:
            self.apply_filters()
            
    def on_filter_text_changed(self, text):
        """Store filter text when it changes"""
        self.filter_text = text
        # Optionally apply filter immediately on each keystroke
        # self.apply_filters()
    
    def apply_filters(self):
        """Apply the current filter to the data"""
        self.current_page = 0  # Reset to first page when filtering
        self.populate_table()

    def populate_table(self):
        """Populates the table with the current filtered data, limited to the current page."""
        # Fetch all data for filtering
        all_members = Controller.get_member_list_data(0, 1000)  # Limit to 1000 members for performance
        
        # Apply filtering if filter text exists
        filtered_data = all_members
        if self.filter_text:
            filtered_data = []
            for member in all_members:
                # Convert the value to string for case-insensitive contains check
                field_value = str(member.get(self.filter_field, "")).lower()
                if self.filter_text.lower() in field_value:
                    filtered_data.append(member)
        
        # Calculate pagination based on filtered data
        total_items = len(filtered_data)
        max_page = max(0, (total_items - 1) // self.items_per_page)
        
        # Adjust current_page if it's out of bounds after filtering
        self.current_page = min(self.current_page, max_page)
        
        # Get the current page of data
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page
        page_data = filtered_data[start_index:end_index]

        # Update button states
        self.previous_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < max_page)

        # Define the columns to extract data
        columns = [
            "member_number", "member_id", "member_status",
            "first_name", "last_name", "membership_exp_date", "healthdec_exp_date"
        ]

        # Populate the table
        self.table.setRowCount(len(page_data))
        for row, user in enumerate(page_data):
            for col, key in enumerate(columns):
                value = str(user.get(key, ""))  # Safely get the value, default to empty string
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Highlight inactive status
                if key == "member_status" and value == "Inactive":
                    item.setForeground(QBrush(QColor(255, 55, 55)))  # Red color for inactive status
                elif key == "member_status" and value == "Active":
                    item.setForeground(QBrush(QColor(76, 175, 80)))  # Green color for active status

                self.table.setItem(row, col, item)
                
        # Show count of filtered results if filtering is active
        if self.filter_text:
            self.table.setHorizontalHeaderLabels([
                f"מספר מנוי ({total_items} תוצאות)", "ת.ז", "סטטוס", "שם פרטי", "שם משפחה", "תפוגת מנוי", "תפוגת אישור בריאות"
            ])
        else:
            self.table.setHorizontalHeaderLabels([
                "מספר מנוי", "ת.ז", "סטטוס", "שם פרטי", "שם משפחה", "תפוגת מנוי", "תפוגת אישור בריאות"
            ])


    def next_page(self):
        """Moves to the next page."""
        # Get filtered data count instead of total
        all_members = Controller.get_member_list_data(0, 1000)
        filtered_data = all_members
        if self.filter_text:
            filtered_data = []
            for member in all_members:
                field_value = str(member.get(self.filter_field, "")).lower()
                if self.filter_text.lower() in field_value:
                    filtered_data.append(member)
                    
        total_items = len(filtered_data)
        max_page = (total_items - 1) // self.items_per_page

        if self.current_page < max_page:
            self.current_page += 1
            self.populate_table()


    def previous_page(self):
        """Moves to the previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_table()



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MemberListWidget()
    window.resize(1200, 600)
    window.show()
    sys.exit(app.exec())
