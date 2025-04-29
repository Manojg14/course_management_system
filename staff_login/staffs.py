# staff.py
from student_login.student import Student
from course_management.course import Course
from course_management.enrollment import Enrollment
from course_management.assignment import Assignment
from course_management.submission import Submission

def get_db_manager(self):
    from database.database_mg import DataBasemanagement
    return DataBasemanagement()

class Staff:
    def __init__(self, staff_id = None, staff_name = None, email = None, phone_no = None, password_hash = None):
            self.staff_id = staff_id
            self.staff_name = staff_name
            self.email = email
            self.phone_no = phone_no
            self.password_hash = password_hash
            self.data_base = get_db_manager(self)

    def staff_display(self):
            return f"User Id:{self.staff_id},User Name:{self.staff_name},Email:{self.email},Phone no:{self.phone_no},Password Hash:{self.password_hash}"

    def __str__(self):
            return self.staff_display()

    def staff_login(self):
            staff_name = input("Enter Staff Username: ")
            password_hash = input("Enter Staff Password: ")
            staff = self.data_base.check_staff_credentials(staff_name, password_hash)
            if staff:
                print("Staff login successful!")
                return True
            else:
                print("Invalid Staff credentials.")
                return False

    def add_staff(self):
            staff_id = int(input(f"Enter Staff ID: "))
            staff_name = input(f"Enter Staff Name: ")
            email = input("Enter User Email: ")
            phone_no = input("Enter the Phone No: ")
            password_hash = input("Enter User Login Password: ")
            staffs = Staff(staff_id, staff_name, email, phone_no, password_hash)
            self.data_base.insert_staff_table(staffs)
            print("Staff Data Added Successfully!..")

    def view_staff(self):

            staff = self.data_base.get_staff_users()
            if not staff:
                print("No staff Available")
            else:
                print("Staff Lists")
                for person in staff:
                    print(person)

    def update_staff(self):
            staff_id = int(input("enter your Staff Id:"))
            changes = input("Enter you want to change(staff name or email or phone no or password hash )")

            if changes == 'staff name':
                staff_name = input("enter update staff name:")
                self.data_base.update_staff_details(staff_id=staff_id, staff_name=staff_name)
                print(f"Staff Name added to staff id {staff_id} Successfully!..")

            elif changes == 'email':
                email = input("enter update email:")
                self.data_base.update_staff_details(staff_id=staff_id, email=email)
                print(f"Email added to Staff id {staff_id} Successfully!..")

            elif changes == 'phone no':
                phone_no = input("enter update phone no:")
                self.data_base.update_staff_details(staff_id=staff_id, phone_no=phone_no)
                print(f"Staff Phone No added to staff id {staff_id} Successfully!..")

            elif changes == 'password hash':
                password_hash = input("enter the update password:")
                self.data_base.update_staff_details(staff_id=staff_id, password_hash=password_hash)
                print(f"Password Hash added to staff id {staff_id} Successfully!..")

            else:
                print("Enter valid choice!...")

    def delete_staffs(self):
            staff_id = int(input("Enter staff Id you want to delete:"))
            if staff_id:
                self.data_base.delete_staff_table(staff_id)
            else:
                print("Information Not Match!..")


# ============================ staff_login =============================================================================

class StaffLogin(Staff,Student,Course,Enrollment,Assignment,Submission):

    def __init__(self):
        Student.__init__(self)
        Staff.__init__(self)
        Course.__init__(self)
        Enrollment.__init__(self)
        Assignment.__init__(self)
        Submission.__init__(self)

    def handle_staff(self):
        if self.staff_login():
            print("\n=================== STAFF LOGIN ===============================")
            print("1. Add\n2. View\n3. Delete\n4. Exit")
            print("=" * 65)
            staff_choice = int(input("Enter your choice: "))

            if staff_choice == 1:
                print("1. Students\n2. Enrollments\n3. Assignments")
                choices = int(input("Enter your Add choice: "))
                if choices == 1:
                    self.add_student()
                elif choices == 2:
                    self.add_enrollment()
                elif choices == 3:
                    self.add_assignment()

            elif staff_choice == 2:
                print("1. Courses\n2. Student\n3. Assignments\n4. Submission")
                view_choice = int(input("Enter your view choice: "))
                if view_choice == 1:
                    self.view_course()

                elif view_choice == 2:
                    condition = input("Enter your choice (all or coursewise): ").strip().lower()
                    if condition == 'all':
                        self.view_enrollments()
                    elif condition == 'coursewise':
                        course_id = int(input("Enter courses ID: "))
                        self.data_base.get_enrollment_details_by_course(course_id)

                elif view_choice == 3:
                    condition = input("Enter your choice (all or coursewise): ").strip().lower()
                    if condition == 'all':
                        self.view_assignment()
                    elif condition == 'coursewise':
                        course_id = int(input("Enter courses ID: "))
                        self.view_assignment(course_id)

                elif view_choice == 4:
                    condition = input("Enter your choice (all or coursewise): ").strip().lower()
                    if condition == 'all':
                        self.view_submission()
                    elif condition == 'coursewise':
                        course_id = int(input("Enter courses ID: "))
                        self.data_base.get_submission_details_by_course(course_id)

            elif staff_choice == 3:
                print("1. Student\n2. Enrollment\n3. Assignment\n4. Submission")
                choices = int(input("Enter your Delete Values: "))
                if choices == 1:
                    self.delete_students()
                elif choices == 2:
                    self.delete_enrollment_details()
                elif choices == 3:
                    self.delete_assignments()
                elif choices == 4:
                    self.delete_submission_details()

            elif staff_choice == 4:
                print("Exiting Staff Panel...")
            else:
                print("Enter valid choice.")
