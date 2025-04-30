import smtplib
from email.mime.text import MIMEText

def get_db_manager(self):
    from database.database_mg import DataBasemanagement
    return DataBasemanagement()

class Payment:
    def __init__(self):

        self.data_base = get_db_manager(self)

    def process_payment(self, student_id):
        enrollments = self.data_base.get_enrollment_by_student_id(student_id)
        if not enrollments:
            print("No enrollment found for this student.")
            return

        print("Enrolled Courses:")
        for courses in enrollments:
            courses = self.data_base.get_course_by_id(courses.course_id)
            print(f"Course ID: {courses.course_id}, Name: {courses.title}, Fee: {courses.course_fee}")

        course_id = int(input("Enter Course ID you want to pay for: "))
        course = self.data_base.get_course_by_id(course_id)
        fee = course.course_fee

        amount_paid = int(input(f"Enter payment amount (Max: {fee}): "))
        status = "Paid" if amount_paid >= fee else "Pending"
        pending_amount = fee - amount_paid if amount_paid < fee else 0

        self.data_base.insert_payment_history(student_id, course_id, amount_paid, pending_amount,status)

        student_id = self.data_base.get_student_by_id(student_id)
        self.display_receipt(student_id, course, amount_paid, pending_amount, status)
        self.send_email_receipt(student_id, course, amount_paid, pending_amount, status)

    def display_receipt(self, student, course, amount_paid, pending, status):
        print("\n====== Payment Receipt ======")
        print(f"Student ID: {student.student_id}")
        print(f"Student Name: {student.student_name}")
        print(f"Course ID: {course.course_id}")
        print(f"Course Name: {course.title}")
        print(f"Total Fee: {course.course_fee}")
        print(f"Amount Paid: {amount_paid}")
        print(f"Pending Amount: {pending}")
        print(f"Payment Status: {status}")
        print("==============================")

    def send_email_receipt(self, student, course, amount_paid, pending, status):
        subject = "Course Payment Receipt"
        message = f"""
        Payment Receipt:

        Student ID: {student.student_id}
        Student Name: {student.student_name}
        Course ID: {course.course_id}
        Course Name: {course.title}
        Total Fee: {course.course_fee}
        Amount Paid: {amount_paid}
        Pending Amount: {pending}
        Payment Status: {status}
        """

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = "kncetppt24@gmail.com"
        msg['To'] = student.email
        admin_email = "manojggm14@gmail.com"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("manojggm14@gmail.com", 'hafrydizwwblhtqo')
            server.sendmail(msg['From'], [msg['To'], admin_email], msg.as_string())
