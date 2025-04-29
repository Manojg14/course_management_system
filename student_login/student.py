# student.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from course_management.assignment import Assignment
from course_management.submission import Submission

def get_db_manager(self):
    from database.database_mg import DataBasemanagement
    return DataBasemanagement()

def get_staff(self):
    from staff_login.staffs import Staff
    return Staff()

class Student:

    def __init__(self, student_id = None, student_name = None, email = None, phone_no = None, password_hash = None):
            self.student_id = student_id
            self.student_name = student_name
            self.email = email
            self.phone_no = phone_no
            self.password_hash = password_hash
            self.data_base = get_db_manager(self)

    def student_display(self):
        return f"User Id:{self.student_id},User Name:{self.student_name},Email:{self.email},Phone no:{self.phone_no},Password Hash:{self.password_hash}"

    def __str__(self):
        return self.student_display()

    def student_login(self):
        student_name = input("Enter Student Username: ")
        password_hash = input("Enter Student Password: ")
        student = self.data_base.check_student_credentials(student_name, password_hash)
        if student:
            print("Student login successful!")
            return True
        else:
            print("Invalid Student credentials.")
            return False

    def add_student(self):
        student_id = int(input(f"Enter Student ID: "))
        student_name = input(f"Enter Student Name: ")
        email = input("Enter User Email: ")
        phone_no = input("Enter the Phone No: ")
        password_hash = input("Enter User Login Password: ")
        students = Student(student_id,student_name, email, phone_no, password_hash)
        self.data_base.insert_student_table(students)
        print("Student Data Added Successfully!..")

    def view_student(self):

        student = self.data_base.get_student_users()
        if not student:
            print("No student Available")
        else:
            print("Student Lists")
            for person in student:
                print(person)

    def update_student(self):
        student_id = int(input("enter your Student Id:"))
        changes = input("Enter you want to change(student name or email or phone no or password hash )")

        if changes == 'student name':
            student_name = input("enter update student name:")
            self.data_base.update_student_details(student_id= student_id, student_name=student_name)
            print(f"Student Name added to student id {student_id} Successfully!..")

        elif changes == 'email':
            email = input("enter update email:")
            self.data_base.update_student_details(student_id=student_id, email=email)
            print(f"Email added to Student id {student_id} Successfully!..")

        elif changes == 'phone no':
            phone_no = input("enter update phone no:")
            self.data_base.update_student_details(student_id=student_id, phone_no=phone_no)
            print(f"Student Phone No added to student id {student_id} Successfully!..")

        elif changes == 'password hash':
            password_hash = input("enter the update password:")
            self.data_base.update_student_details(student_id=student_id, password_hash=password_hash)
            print(f"Password Hash added to student id {student_id} Successfully!..")

        else:
            print("Enter valid choice!...")

    def delete_students(self):
        student_id = int(input("Enter student Id you want to delete:"))
        if student_id:
            self.data_base.delete_student_table(student_id)
        else:
            print("Information Not Match!..")

# ============================ student_login =============================================================================

class StudentLogin(Student,Assignment,Submission):

    def handle_student(self):
        if self.student_login():
            print("\n=================== STUDENT LOGIN ===============================")
            print("1. Assignment\n2. Submit\n3. Query\n4. Exit")
            print("=" * 70)
            student_choice = int(input("Enter your choice: "))

            if student_choice == 1:
                course_id = int(input("Enter your courses ID: "))
                self.view_assignment(course_id)

            elif student_choice == 2:
                self.add_submission()

            elif student_choice == 3:
                student_id = input("Enter your Student ID: ").strip()
                course_id = input("Enter Course ID: ").strip()
                email = self.data_base.get_staff_email_by_enrollment(student_id, course_id)
                if email:
                    student_email = input("Enter your email: ").strip()
                    subject = input("Enter subject: ").strip()
                    message = input("Enter your query message: ").strip()
                    msg = MIMEMultipart()
                    msg['From'] = student_email
                    msg['To'] = email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(message, 'plain'))

                    try:
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        sender_password = 'hafrydizwwblhtqo'
                        server.login(student_email, sender_password)
                        server.sendmail(student_email, email, msg.as_string())
                        server.quit()
                        print("Email sent successfully!")
                    except Exception as e:
                        print("Failed to send email:", e)
                else:
                    print("Unable to retrieve staff email.")

            elif student_choice == 4:
                print("Exiting Student Panel...")

