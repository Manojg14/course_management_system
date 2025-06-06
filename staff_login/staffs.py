# staff.py
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime,timedelta

from student_login.student import Student
from course_management.course import Course
from course_management.enrollment import Enrollment
from course_management.assignment import Assignment
from course_management.submission import Submission
from course_management.forum import Forum

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


    def generate_otp(self, length=6):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    def send_otp_email(self, to_email, user_type = 'Staff'):
        sender_email = "manojggm14@gmail.com"
        app_password = "hafrydizwwblhtqo"
        otp = self.generate_otp()

        subject = f"OTP for {user_type} Login"
        body = f"Dear {user_type},\n\nYour OTP for login is: {otp}\n\nRegards,\nInstitute Admin"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.quit()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Email sent to {to_email}")
            print("OTP is valid for 1 minutes.")
            return otp, datetime.now()
        except Exception as e:
            print("Failed to send OTP email:", e)


    def staff_login(self):
            staff_id = input("Enter Staff UserId: ")
            password_hash = input("Enter Staff Password: ")
            staff = self.data_base.check_staff_credentials(staff_id, password_hash)
            if staff:
                print("Credentials verified. Sending OTP...")
                staff_email = staff[2]

                otp, otp_sent_time = self.send_otp_email(to_email= staff_email, user_type='Staff')

                entered_otp = input("Enter the OTP sent to your email: ")
                current_time = datetime.now()

                if current_time - otp_sent_time > timedelta(minutes=1):
                    print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] OTP expired.")
                    return False
                elif entered_otp == otp:
                    print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Staff login successful!")
                    return True
                else:
                    print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Invalid OTP. Access denied.")
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

class StaffLogin(Staff,Student,Course,Enrollment,Assignment,Submission,Forum):

    def __init__(self):
        Student.__init__(self)
        Staff.__init__(self)
        Course.__init__(self)
        Enrollment.__init__(self)
        Assignment.__init__(self)
        Submission.__init__(self)
        Forum.__init__(self)

    def handle_staff(self):
        if self.staff_login():
            print("\n=================== STAFF LOGIN ===============================")
            print("1. Add\n2. View\n3. Delete\n4. Forum\n5. Exit")
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
                    print("1. View Forum\n2. Post Message\n3. Reply to a Message")
                    choice = input("Enter choice: ")
                    if choice == '1':
                        condition = input("Enter your choice (all or coursewise): ").strip().lower()
                        if condition == 'all':
                            self.view_forum()
                        elif condition == 'coursewise':
                            course_id = int(input("Enter courses ID: "))
                            self.view_forum(course_id)
                    elif choice == '2':
                        self.add_forum_message()
                        print("Message Posted")
                    elif choice == '3':
                        self.post_reply()
                        print("Reply Message send Successfully!...")


            elif staff_choice == 4:
                print("Exiting Staff Panel...")
            else:
                print("Enter valid choice.")
