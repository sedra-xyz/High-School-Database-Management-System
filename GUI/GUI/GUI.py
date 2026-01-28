import tkinter as tk
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DeedraDBApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Deedra High School Database Management System")

        self.label_user_id = tk.Label(master, text="User ID:")
        self.label_user_id.grid(row=0, column=0)
        self.entry_user_id = tk.Entry(master)
        self.entry_user_id.grid(row=0, column=1)

        self.label_role = tk.Label(master, text="Role:")
        self.label_role.grid(row=1, column=0)
        self.entry_role = tk.Entry(master)
        self.entry_role.grid(row=1, column=1)

        self.button_login = tk.Button(master, text="Login", command=self.login)
        self.button_login.grid(row=2, columnspan=2)

        # Database connection - using environment variables
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME', 'deedrahighschool')
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            tk.messagebox.showerror("Database Error", "Failed to connect to database. Please check your credentials.")


    def login(self):
        user_id = self.entry_user_id.get()
        role = self.entry_role.get()
        self.create_menu(role, user_id)

    def create_menu(self, user_role, user_id):
        self.clear_screen()
        self.label_welcome = tk.Label(self.master, text=f"Welcome to Deedra High School DBMS, {user_role}!")
        self.label_welcome.grid(row=0, columnspan=2)

        # Add buttons for different actions based on user role
        actions = self.get_actions(user_role)
        for i, action in enumerate(actions):
            button = tk.Button(self.master, text=action, command=lambda action=action: self.handle_action(action, user_role, user_id))
            button.grid(row=i+1, columnspan=2)

    def handle_action(self, action, user_role, user_id):
        if action == "View grades":
            self.view_information("grade", user_role, user_id)
        elif action == "View submissions":
            self.view_information("submission", user_role, user_id)
        elif action == "View assignments":
            self.view_information("assignment", user_role, user_id)
        elif action == "View exams":
            self.view_information("exam", user_role, user_id)
        elif action == "Add grades":
            self.add_information("grade", user_role)
        elif action == "Edit grades":
            self.edit_information("grade", user_role)
        elif action == "Add assignments":
            self.add_information("assignment", user_role)
        elif action == "Edit assignments":
            self.edit_information("assignment", user_role)
        elif action == "Exit":
            self.master.quit()

    def view_information(self, table_name, user_role, user_id=None):
        self.clear_screen()
        columns = self.get_table_columns(table_name)
        label_columns = tk.Label(self.master, text=f"Columns in {table_name}: {', '.join(columns)}")
        label_columns.grid(row=0, columnspan=2)

        result = self.select_from_table(table_name, user_role, user_id)
        if result:
            for i, row in enumerate(result):
                label_row = tk.Label(self.master, text=row)
                label_row.grid(row=i+1, columnspan=2)
        else:
            label_no_records = tk.Label(self.master, text=f"No records found in the {table_name} table for the current user.")
            label_no_records.grid(row=1, columnspan=2)

    def add_information(self, table_name, user_role):
        self.clear_screen()
        columns = self.get_table_columns(table_name)
        label_columns = tk.Label(self.master, text=f"Columns in {table_name}: {', '.join(columns)}")
        label_columns.grid(row=0, columnspan=2)

        values = []
        for i, column in enumerate(columns):
            label = tk.Label(self.master, text=f"{column}:")
            label.grid(row=i+1, column=0)
            entry = tk.Entry(self.master)
            entry.grid(row=i+1, column=1)
            values.append(entry)

        button_submit = tk.Button(self.master, text="Submit", command=lambda: self.insert_into_table(table_name, [entry.get() for entry in values], user_role))
        button_submit.grid(row=len(columns)+1, columnspan=2)

    def edit_information(self, table_name, user_role):
        pass  # Implement this based on your requirements

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def get_actions(self, user_role):
        if user_role == "Student":
            return ["View grades", "View submissions", "View assignments", "View exams", "Exit"]
        elif user_role == "Teacher":
            return ["View grades", "View submissions", "View assignments", "View exams",
                    "Add grades", "Edit grades", "Add assignments", "Edit assignments", "Exit"]
        elif user_role == "Coordinator":
            return ["View grades", "View submissions", "View assignments", "View exams",
                    "Add subjects", "Edit subjects", "Delete subjects", "Add exams", "Edit exams",
                    "Delete exams", "Add assignments", "Edit assignments", "Delete assignments",
                    "Add predicted grades", "Edit predicted grades", "Delete predicted grades",
                    "Add grades", "Edit grades", "Delete grades", "Exit"]
        elif user_role == "Administrator":
            return ["View administrates", "View assigned", "View assignment", "View class",
                    "View coordinates", "View employee", "View exam", "View grade", "View predictgrade",
                    "View student", "View subject", "View submission", "View takeexam", "View teaches",
                    "View teaching", "Add record", "Edit record", "Delete record", "Exit"]
        else:
            return []

    def select_from_table(self, table_name, user_role, user_id=None):
        if table_name not in ["student", "teacher", "class", "teaching", "assigned", "subject", "exam", "submission", "coordinates", "administrates", "predictgrade", "grade"]:
            print("Invalid table name.")
            return []

        if user_role == "Student" and "StudentID" not in self.get_table_columns(table_name):
            print(f"The table {table_name} does not have a StudentID column.")
            return []

        if user_role == "Student":
            query = f"SELECT * FROM {table_name} WHERE StudentID = %s"
            self.cursor.execute(query, (user_id,))
        elif user_role == "Teacher":
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
        elif user_role in ["Coordinator", "Administrator"]:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
        else:
            print("Invalid user role.")
            return []
        return self.cursor.fetchall()

    def get_table_columns(self, table_name):
        self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        return [column[0] for column in self.cursor.fetchall()]

    def insert_into_table(self, table_name, values, user_role):
        if user_role in ["Teacher", "Coordinator", "Administrator"]:
            columns = self.get_table_columns(table_name)
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
            self.cursor.execute(query, values)
            self.connection.commit()
        else:
            print("You don't have permission to insert data.")

def main():
    root = tk.Tk()
    app = DeedraDBApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()