import sys
import os
from pathlib import Path
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QToolBar, QWidgetAction, 
    QPushButton, QSizePolicy, QStackedWidget
)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QIcon, QPixmap
from qt_material import apply_stylesheet

from views.login_window import LoginWindow
from views.MemberListWidget import MemberListWidget
from views.MemberTrackingWidget import MemberTrackingWidget
from views.AddMemberWidget import AddMemberWidget
from controllers.controller import Controller

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        screen_geometry = QApplication.instance().primaryScreen().geometry()

        # Set window size to 90% of screen width and height
        window_width = int(screen_geometry.width() * 0.9)
        window_height = int(screen_geometry.height() * 0.9)
        # Calculate the position to center the window
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

        self.setWindowTitle("Gym Management System")
        
        # Create a stacked widget and set it as the central widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Add your different views/widgets here
        self.default_widget = QWidget()
        self.member_tracking_widget = MemberTrackingWidget(self)
        self.user_list_widget = MemberListWidget()
        self.add_member_widget = AddMemberWidget(self)
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.default_widget)
        self.stacked_widget.addWidget(self.member_tracking_widget)
        self.stacked_widget.addWidget(self.user_list_widget)
        self.stacked_widget.addWidget(self.add_member_widget)

        self.stacked_widget.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Set up the menu bar and toolbar
        self.setup_menus()

    def setup_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&ראשי')
        file_menu.addAction('יציאה', self.destroy)

        system_menu = menu_bar.addMenu('&כניסת מנהל')
        system_menu.addAction('Admin Login', lambda: self.open_admin_login())

        info_menu = menu_bar.addMenu('&מידע')
        info_menu.addAction('מדריך', lambda: self.open_user_guide())
        menu_bar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # Tool bar section
        toolbar = QToolBar('Main toolbar')
        toolbar.setOrientation(Qt.Orientation.Vertical)  # Keep vertical toolbar
        toolbar.setFixedWidth(200)
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolbar)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        icon_files = [
            ("resources/icons/tracking.svg", "מעקב מנויים"),
            ("resources/icons/list.svg", "כל המנויים"),
            ("resources/icons/add.svg", "הוספת מנוי"),
            ("resources/icons/home.svg", "ראשי")
        ]

        for i, (icon_file, title) in enumerate(icon_files):
            button = QPushButton(title)
            button.setIcon(self.create_svg_icon(icon_file))
            button.setStyleSheet("height: 60px; width: 100%; margin: 2px; padding-left: 15px; padding-right: 15px;")
            button.clicked.connect(lambda _, idx=i: self.toolbar_action(idx))
            action = QWidgetAction(self)
            action.setDefaultWidget(button)
            toolbar.addAction(action)

    def create_svg_icon(self, svg_file_path):
        # SVG renderer
        renderer = QSvgRenderer(svg_file_path) 

        # Create a QPixmap with a specific size
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)

        # SVG to pixmap
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def toolbar_action(self, idx):
        if idx == 0:
            self.stacked_widget.setCurrentWidget(self.member_tracking_widget)  # Show MemberTrackingWidget
        elif idx == 1:
            self.stacked_widget.setCurrentWidget(self.user_list_widget)  # Show UserListWidget
        elif idx == 2:
            self.stacked_widget.setCurrentWidget(self.add_member_widget)  # Show AddMemberWidget
        else:
            self.stacked_widget.setCurrentWidget(self.default_widget)  # Show DefaultWidget

    #-------------------------------------
    # Menu bar actions
    def open_admin_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()

    def open_user_guide(self):
        pass

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(Path('stylesheet.qss').read_text())
    main_window = MainWindow()
    main_window.show()
    app.exec()
