# Gym Management System

A comprehensive gym management application built as a self-learning project to explore MVC architecture and database design principles.

![Gym Management System]

## Project Overview

This application provides a complete solution for gym owners to manage their members, track attendance, and handle membership details. It features a modern, responsive UI with right-to-left (RTL) support for Hebrew language.

## Features

- Member management (add, view, search)
- Attendance tracking with timestamps
- Membership expiration management
- Status tracking (active/inactive members)
- Modern dark-themed UI with responsive design
- Right-to-left (RTL) language support

## Technologies Used

- **Python** - Core programming language
- **PyQt6** - UI framework for desktop application
- **SQLite** - Lightweight database for storing member data
- **MVC Architecture** - Separation of concerns with Models, Views, and Controllers

## Learning Goals

This project was created as a self-learning exercise to practice:

1. **MVC Architecture** - Implementing a clean separation between data models, business logic, and UI presentation
2. **Database Design** - Creating efficient database schemas and implementing CRUD operations
3. **UI/UX Design** - Building a modern, responsive interface with dark theme
4. **Input Validation** - Implementing proper form validation and error handling

## Project Structure

The application follows the MVC (Model-View-Controller) pattern:

- **Models** - Define data structures and database operations
- **Views** - Handle the UI components and user interactions
- **Controllers** - Manage communication between views and models

```
gym_manager/
├── models/          # Data models and database operations
├── views/           # UI components
├── controllers/     # Business logic
├── resources/       # Icons and other resources
└── data/            # Database files
```

## Getting Started

1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Run the application: `python app.py` 