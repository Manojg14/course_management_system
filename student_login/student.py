# student.py
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime,timedelta


from course_management.assignment import Assignment
from course_management.submission import Submission
from course_management.forum import Forum
from payments.payment_process import Payment

def get_db_manager(self):
    from database.database_mg import DataBasemanagement
    return DataBasemanagement()

def get_staff():
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

    def generate_otp(self, length=6):
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    def send_otp_email(self, to_email, user_type = 'Student'):
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

    def student_login(self):

        student_id = input("Enter Student UserId: ")
        password_hash = input("Enter Student Password: ")
        student = self.data_base.check_student_credentials(student_id, password_hash)
        if student:
            print("Credentials verified. Sending OTP...")
            student_email = student[2]

            otp,otp_sent_time =self.send_otp_email(to_email=student_email,user_type='Student')

            entered_otp = input("Enter the OTP sent to your email: ")
            current_time = datetime.now()

            if current_time - otp_sent_time > timedelta(minutes=1):
                print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] OTP expired.")
                return False
            elif entered_otp == otp:
                print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Student login successful!")
                return True
            else:
                print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Invalid OTP. Access denied.")
                return False
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
            self.data_base.update_student_details(student_id = student_id, phone_no = phone_no)
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

class StudentLogin(Student,Assignment,Submission,Forum):

    def handle_student(self):
        if self.student_login():
            print("\n=================== STUDENT LOGIN ===============================")
            print("1. Assignment\n2. Submit\n3. Query\n4. Forum\n5. Payment\n6. Exit")
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

            elif student_choice == 5:
                payment_handler = Payment()
                student_id = int(input("Enter your Student ID: "))
                payment_handler.process_payment(student_id)



            elif student_choice == 6:
                print("Exiting Student Panel...")


