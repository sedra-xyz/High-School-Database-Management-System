#High School Database Management System

A role-based database management system for managing high school academic records, built with Python, MySQL, and Tkinter.

##  Description

Deedra High School DBMS is a comprehensive database application designed to streamline academic administration in high schools. The system provides role-based access control, allowing students, teachers, coordinators, and administrators to interact with academic data according to their permissions. Built with a user-friendly GUI interface, it simplifies tasks like grade management, assignment tracking, exam scheduling, and student enrollment.

##  Features

### Role-Based Access Control
- **Students**: View grades, submissions, assignments, and exams
- **Teachers**: View and manage grades, assignments, and submissions
- **Coordinators**: Full control over subjects, exams, assignments, predicted grades, and grades
- **Administrators**: Complete system access with full CRUD operations on all tables

### Key Functionalities
- 📊 Grade management and tracking
- 📝 Assignment creation and submission monitoring
- 📚 Exam scheduling and administration
- 👥 Student enrollment and class assignment
- 📈 Predicted grade tracking
- 🔐 Secure role-based authentication
- 💾 Real-time database operations

##  Technologies Used

- **Python 3.x**: Core programming language
- **MySQL/MariaDB**: Database management system
- **Tkinter**: GUI framework
- **mysql-connector-python**: Database connectivity

## Project Structure

```
deedra-highschool-dbms/
├── GUI.py                    # Tkinter-based graphical interface
├── DeedraHighschool.py       # Command-line interface version
├── DeedraHS.sql              # Database schema and sample data
├── DeedraHighschool.sln      # Visual Studio solution file
├── DeedraHighschool.pyproj   # Python project file
├── GUI.sln                   # GUI solution file
└── GUI.pyproj                # GUI project file
```

## 📊 Database Schema

The system includes the following main tables:

- **student**: Student information and records
- **teacher**: Teacher/employee information
- **subject**: Course subjects
- **class**: Class sections
- **assignment**: Assignment details
- **exam**: Examination information
- **grade**: Student grades
- **submission**: Assignment submissions
- **predictgrade**: Predicted grades
- **teaching**: Teacher-subject assignments
- **assigned**: Student-class assignments
- **coordinates**: Coordinator assignments
- **administrates**: Administrator assignments

##  Installation

### Prerequisites

- Python 3.x installed on your system
- MySQL or MariaDB server
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/deedra-highschool-dbms.git
   cd deedra-highschool-dbms
   ```

2. **Install required Python packages**
   ```bash
   pip install mysql-connector-python
   ```

3. **Set up the database**
   - Start your MySQL/MariaDB server
   - Import the database schema:
   ```bash
   mysql -u your_username -p < DeedraHS.sql
   ```

4. **Configure database credentials**
   
   Update the database connection settings in both `GUI.py` and `DeedraHighschool.py`:
   ```python
   connection = mysql.connector.connect(
       host='localhost',
       user='your_username',      # Change this
       password='your_password',  # Change this
       database='deedrahighschool'
   )
   ```

##  Usage

### Running the GUI Version

```bash
python GUI.py
```

1. Enter your User ID (e.g., S001 for students, T001 for teachers)
2. Enter your Role (Student, Teacher, Coordinator, or Administrator)
3. Click "Login" to access the system
4. Navigate through available options based on your role

### Running the Command-Line Version

```bash
python DeedraHighschool.py
```

Follow the on-screen prompts to interact with the system.

## Sample User Roles

### Example User IDs
- **Students**: S001, S002, S003, etc.
- **Teachers**: T001, T002, T003, etc.
- **Coordinators**: C001, C002, C003, etc.
- **Administrators**: A001, A002, A003, etc.

## Security Notes

⚠️ **Important**: The current implementation includes hardcoded database credentials for demonstration purposes. For production use:

- Remove hardcoded credentials
- Implement environment variables or configuration files
- Use password hashing for user authentication
- Implement proper SQL injection prevention
- Add input validation and sanitization

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  Future Enhancements

- [ ] User authentication with password hashing
- [ ] PDF report generation
- [ ] Email notifications for grades and assignments
- [ ] Advanced search and filtering
- [ ] Data visualization and analytics dashboard
- [ ] Mobile application version
- [ ] Attendance tracking system
- [ ] Parent portal access

##  License

This project is available for educational purposes. Please add an appropriate license based on your requirements.

##  Acknowledgments

- Thanks to all contributors who have helped shape this project
- Inspired by the need for efficient academic management systems
- Built as a learning project for database management and GUI development

---

**Note**: This is an educational project. Ensure proper security measures are implemented before using in a production environment.
