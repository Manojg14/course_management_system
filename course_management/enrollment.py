# enrollment.py

from ... course_management_system.database.database_mg import DataBasemanagement

class Enrollment:

    def __init__(self, enrollment_id=None, student_id=None, course_id=None):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.data_base = DataBasemanagement()

    def enrollment_display(self):
        return f"Enrollment Id:{self.enrollment_id},Student Id:{self.student_id},Course Id:{self.course_id}"

    def __str__(self):
        return self.enrollment_display()

    def add_enrollment(self):
        enrollment_id = int(input("Enter Enrollment ID: "))
        student_id = int(input("Enter Your Student ID: "))
        course_id = int(input("Enter Course ID to Enroll: "))
        enrollments = Enrollment(enrollment_id, student_id, course_id)
        self.data_base.insert_enrollment_table(enrollments)


    def view_enrollments(self):
        choice = input("Enter your choice (all or coursewise): ").strip().lower()
        if choice == "all":
            rows = self.data_base.get_enrollment_details()
            print(rows)
        elif choice == "coursewise":
            course_id = input("Enter courses ID: ").strip()
            rows = self.data_base.get_enrollment_details_by_course(course_id=course_id)
            print(rows)
        else:
            print("Invalid choice")
            return

    def delete_enrollment_details(self):
        enrollment_id = int(input("Enter enrollment Id you want to delete:"))
        if self.data_base.delete_enrollment(enrollment_id):
            print(f"Enrollment Id {enrollment_id} deleted successfully!..")
        else:
            print(f"Enrollment Id {enrollment_id} not found")

