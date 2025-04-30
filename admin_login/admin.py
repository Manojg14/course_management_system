# admin.py

from database.database_mg import DataBasemanagement
from student_login.student import Student
from staff_login.staffs import Staff
from course_management.course import Course
from course_management.enrollment import Enrollment


class Admin:

    def __init__(self,admin_id = None, admin_name = None, password_hash = None):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.password_hash = password_hash
        self.data_base = DataBasemanagement()

    def login(self):
        if self.admin_name == "admin" and self.password_hash == "admin123":
            print("Admin login successful!")
            return True
        else:
            print("Invalid credentials!")
            return False

    def add_admin(self):
        admin_id = int(input("enter admin id:"))
        admin_name = input("enter admin name:")
        password_hash = input("enter admin password:")
        admins = Admin(admin_id,admin_name,password_hash)
        self.data_base.insert_admin_table(admins)
        print("Admin Added Successfully!...")

    def view_admin(self):

            admin = self.data_base.get_admin_users()
            if not admin:
                print("No Admins Available")
            else:
                print("Admin Lists")
                for person in admin:
                    print(person)

    def delete_admins(self):
            admin_id = int(input("Enter admin Id you want to delete:"))
            if admin_id:
                self.data_base.delete_admin_table(admin_id)
            else:
                print("Information Not Match!..")


class AdminLogin(Admin,Student,Staff,Course,Enrollment):

    class AdminLogin(Admin, Student, Staff, Course, Enrollment):
        def __init__(self):
            Admin.__init__(self)
            Student.__init__(self)
            Staff.__init__(self)
            Course.__init__(self)
            Enrollment.__init__(self)

    def handle_admin(self):
        print("\n=================== ADMIN LOGIN ===============================")
        print("1. Add")
        print("2. View")
        print("3. Update")
        print("4. Delete")
        print("5. Payments")
        print("=" * 65)

        admin_choice = int(input("Enter your choice: "))

        if admin_choice == 1:
           print("1. Admin\n2. Course\n3. Staff\n4. Student")
           choice = int(input("Enter your choice to add values: "))
           if choice == 1:
               self.add_admin()
           elif choice == 2:
               self.add_course()
           elif choice == 3:
               self.add_staff()
           elif choice == 4:
               self.add_student()

        elif admin_choice == 2:
            print("1. Course\n2. Staff\n3. Student\n4. Enrollment")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                self.view_course()
            elif choice == 2:
                self.view_staff()
            elif choice == 3:
                self.view_student()
            elif choice == 4:
                self.view_enrollments()
            else:
                print("Invalid view choice.")

        elif admin_choice == 3:
            print("1. Course\n2. Staff\n3. Student")
            choice = int(input("Enter your choice to update values: "))
            if choice == 1:
                self.update_courses()
            elif choice == 2:
                self.update_staff()
            elif choice == 3:
                self.update_student()

        elif admin_choice == 4:
            print("1. Admin\n2. Course\n3. Staff\n4. Student")
            choice = int(input("Enter your choice to delete values: "))
            if choice == 1:
                self.delete_admins()
            if choice == 2:
                self.delete_course_details()
            elif choice == 3:
                self.delete_staffs()
            elif choice == 4:
                self.delete_students()

        elif admin_choice == 5:
            payments = self.data_base.get_all_payments()
            print("\n========== Payment History ==========")
            for row in payments:
                print(f"""
            Payment ID:      {row[0]}
            Student ID:      {row[1]}
            Student Name:    {row[2]}
            Course ID:       {row[3]}
            Course Name:     {row[4]}
            Amount Paid:     ₹{row[5]}
            Pending Amount:  ₹{row[6]}
            Status:          {row[7]}
            Payment Date:    {row[8]}
            ---------------------------------------
                    """)
            print("=====================================")

        else:
            print("Enter a valid number!")






