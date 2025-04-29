# course.py

from ... course_management_system.database.database_mg import DataBasemanagement

class Course:

    def __init__(self,course_id = None,title = None,description = None,max_enrollment = None,course_fee = None, staff_id = None):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.max_enrollment = max_enrollment
        self.course_fee = course_fee
        self.staff_id = staff_id
        self.data_base = DataBasemanagement()

    def course_display(self):
        return f"Course Id:{self.course_id},Title:{self.title},Description:{self.description}Max Enrollment:{self.max_enrollment},Course Fee:{self.course_fee},Staff Id:{self.staff_id}"

    def __str__(self):
        return self.course_display()

    def add_course(self):
        course_id = int(input("Enter Course ID:"))
        title = input("Enter Course Name:")
        description = input("Enter Course Description:")
        max_enrollment = int(input("Enter max Enrollment"))
        course_fee = float(input("Enter courses Price:"))
        staff_id = int(input("Enter Staff Id:"))
        courses = Course(course_id, title, description, max_enrollment, course_fee, staff_id)
        self.data_base.insert_course_table(courses)
        print("Course Added Successfully!...")

    def view_course(self):
        courses = self.data_base.search_student_course()
        if not courses:
            print("NO courses are Available")
        else:

            print("Available Course List")
            for row in courses:
                print(row)

    def update_courses(self):
        course_id = int(input("enter your Course Id:"))
        changes = input("Enter you want to change(title or description or max enrollment or courses fee or staff id)")

        if changes == 'title':
            title = input("enter update courses name:")
            self.data_base.update_course_details( title= title,course_id=course_id)
            print(f"Course Name added to courses id {course_id} Successfully!..")

        elif changes == 'description':
            description = input("enter update description:")
            self.data_base.update_course_details(course_id=course_id, description=description)
            print(f"Course Description added to courses id {course_id} Successfully!..")

        elif changes == 'max enrollment':
            max_enrollment = int(input("enter update max enrollment"))
            self.data_base.update_course_details(course_id=course_id, max_enrollment=max_enrollment)
            print(f"Course Max Enrollment added to courses id {course_id} Successfully!..")

        elif changes == 'courses fee':
            course_fee = float(input("enter the update courses fee:"))
            self.data_base.update_course_details(course_id=course_id, course_fee=course_fee)
            print(f"courses fee added to courses id {course_id} Successfully!..")

        elif changes == 'staff id':
            staff_id = int(input("enter the update staff id:"))
            self.data_base.update_course_details(course_id = course_id, staff_id = staff_id)
        else:
            print("Enter valid choice!...")

    def delete_course_details(self):
        course_id = int(input("Enter courses Id you want to delete:"))
        if self.data_base.delete_course(course_id):
            print(f"Course Id {course_id} deleted successfully!..")
        else:
            print(f"Course Id {course_id} not found")


