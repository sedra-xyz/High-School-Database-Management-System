import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Establish connection to the database - using environment variables
deedrahighschool = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'deedrahighschool')
)

# Function to execute SELECT query on a table
def select_from_table(cursor, table_name, user_role, user_id=None):
    if table_name not in ["student", "teacher", "class", "teaching", "assigned", "subject", "exam", "submission", "coordinates", "administrates", "predictgrade", "grade"]:
        print("Invalid table name.")
        return []

    if user_role == "Student" and "StudentID" not in get_table_columns(cursor, table_name):
        print(f"The table {table_name} does not have a StudentID column.")
        return []

    if user_role == "Student":
        query = f"SELECT * FROM {table_name} WHERE StudentID = %s"
        cursor.execute(query, (user_id,))
    elif user_role == "Teacher":
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
    elif user_role in ["Coordinator", "Administrator"]:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
    else:
        print("Invalid user role.")
        return []
    return cursor.fetchall()

# Function to get column names of a table
def get_table_columns(cursor, table_name):
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    return [column[0] for column in cursor.fetchall()]



def insert_into_table(cursor, table_name, values, user_role):
    if user_role in ["Teacher", "Coordinator", "Administrator"]:
        # Get the columns of the table
        columns = get_table_columns(cursor, table_name)
        
        # Construct the query with placeholders for the filtered values
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
        print("Query:", query)  # Print the query for debugging purposes
        print("Values:", values)  # Print the values for debugging purposes

        # Execute the query with filtered values
        cursor.execute(query, values)
    else:
        print("You don't have permission to insert data.")

def update_table(cursor, table_name, primary_key, column, new_value, user_role):
    try:
        if user_role in ["Teacher", "Coordinator", "Administrator"]:
            query = f"UPDATE {table_name} SET {column} = %s WHERE {primary_key} = %s"
            cursor.execute(query, (new_value, primary_key))
            deedrahighschool.commit()  # Commit the transaction
        else:
            print("You don't have permission to update data.")
    except Exception as e:
        print("An error occurred while updating the record:", e)


# Function to execute DELETE query on a table
def delete_from_table(cursor, table_name, primary_key, user_role):
    if user_role in ["Coordinator", "Administrator"]:
        query = f"DELETE FROM {table_name} WHERE {table_name}ID = %s"
        cursor.execute(query, (primary_key,))
    else:
        print("You don't have permission to delete data.")

# Function to handle the menu
def menu(user_role):
    print("Welcome to Deedra High School Database Management System")
    if user_role == "Student":
        print("1. View grades")
        print("2. View submissions")
        print("3. View assignments")
        print("4. View exams")
        print("5. Exit")
    elif user_role == "Teacher":
        print("1. View grades")
        print("2. View submissions")
        print("3. View assignments")
        print("4. View exams")
        print("5. Add grades")
        print("6. Edit grades")
        print("7. Add assignments")
        print("8. Edit assignments")
        print("9. Exit")
    elif user_role == "Coordinator":
        print("1. View grades")
        print("2. View submissions")
        print("3. View assignments")
        print("4. View exams")
        print("5. Add subjects")
        print("6. Edit subjects")
        print("7. Delete subjects")
        print("8. Add exams")
        print("9. Edit exams")
        print("10. Delete exams")
        print("11. Add assignments")
        print("12. Edit assignments")
        print("13. Delete assignments")
        print("14. Add predicted grades")
        print("15. Edit predicted grades")
        print("16. Delete predicted grades")
        print("17. Add grades")
        print("18. Edit grades")
        print("19. Delete grades")
        print("20. Exit")
    elif user_role == "Administrator":
        print("1. View administrates")
        print("2. View assigned")
        print("3. View assignment")
        print("4. View class")
        print("5. View coordinates")
        print("6. View employee")
        print("7. View exam")
        print("8. View grade")
        print("9. View predictgrade")
        print("10. View student")
        print("11. View subject")
        print("12. View submission")
        print("13. View takeexam")
        print("14. View teaches")
        print("15. View teaching")
        print("16. Add record")
        print("17. Edit record")
        print("18. Delete record")
        print("19. Exit")

def main():
    cursor = deedrahighschool.cursor()
    
    # Get user role
    user_role = input("Enter your role (Student/Teacher/Coordinator/Administrator): ")
    user_id = None
    if user_role == "Student":
        user_id = input("Enter your Student ID: ")
    
    while True:
        menu(user_role)
        choice = input("Enter your choice: ")
        
        if user_role == "Student":
            if choice == "1":
                result = select_from_table(cursor, "grade", user_role, user_id)
                print(result)
            elif choice == "2":
                result = select_from_table(cursor, "submission", user_role, user_id)
                print(result)
            elif choice == "3":
                result = select_from_table(cursor, "assignment", user_role, user_id)
                print(result)
            elif choice == "4":
                result = select_from_table(cursor, "exam", user_role, user_id)
                print(result)
            elif choice == "5":
                break
        
        elif user_role == "Teacher":
            if choice == "1":
                result = select_from_table(cursor, "grade", user_role)
                print(result)
            elif choice == "2":
                result = select_from_table(cursor, "submission", user_role)
                print(result)
            elif choice == "3":
                result = select_from_table(cursor, "assignment", user_role)
                print(result)
            elif choice == "4":
                result = select_from_table(cursor, "exam", user_role)
                print(result)
            elif choice == "5":
                # Add grade
                columns = get_table_columns(cursor, "grade")
                print(f"Enter values for columns: {columns}")
                values = [input(f"{col}: ") for col in columns]
                insert_into_table(cursor, "grade", values, user_role)
                deedrahighschool.commit()
            elif choice == "6":
                # Edit grade
                grade_id = input("Enter Grade ID to edit: ")
                column = input("Enter column name to update: ")
                new_value = input("Enter new value: ")
                update_table(cursor, "grade", grade_id, column, new_value, user_role)
            elif choice == "7":
                # Add assignment
                columns = get_table_columns(cursor, "assignment")
                print(f"Enter values for columns: {columns}")
                values = [input(f"{col}: ") for col in columns]
                insert_into_table(cursor, "assignment", values, user_role)
                deedrahighschool.commit()
            elif choice == "8":
                # Edit assignment
                assignment_id = input("Enter Assignment ID to edit: ")
                column = input("Enter column name to update: ")
                new_value = input("Enter new value: ")
                update_table(cursor, "assignment", assignment_id, column, new_value, user_role)
            elif choice == "9":
                break
        
        elif user_role in ["Coordinator", "Administrator"]:
            # Implement coordinator and administrator functionalities
            if choice == "20" or choice == "19":  # Exit
                break
            else:
                print("Feature under development")
    
    cursor.close()
    deedrahighschool.close()

if __name__ == "__main__":
    main()