# assignment.py
from datetime import datetime
from ... course_management_system.database.database_mg import DataBasemanagement

class Assignment:

    def __init__(self, assignment_id = None, course_id = None, title = None, description = None, due_date = None, assignment_type = None):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assignment_type = assignment_type
        self.data_base = DataBasemanagement()

    def assignment_display(self):
        return f"Assignment Id:{self.assignment_id},Course Id:{self.course_id},Title:{self.title},Description:{self.description},Due Date:{self.due_date},Assignment Type:{self.assignment_type}"

    def add_assignment(self):
        assignment_id = int(input("Enter Assignment ID: "))
        course_id = int(input("Enter Course ID: "))
        title = input("Enter Assignment Title: ")
        description = input("Enter Assignment Description: ")
        try:
            due_date_input = input("Enter Due Date (YYYY-MM-DD HH:MM:SS): ")
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD HH:MM:SS")
            return

        assignment_type = input("Enter Assignment Type (quiz/project/homework): ").lower().strip()
        if assignment_type not in ['quiz', 'project', 'homework']:
            print("Invalid assignment type. Must be quiz/project/homework.")
            return
        assignments = Assignment(assignment_id, course_id, title, description, due_date, assignment_type)
        self.data_base.insert_assignment_table(assignments)
        print("Assignment Added Successfully!..")

    def view_assignment(self, course_id=None):
        if course_id is None:
            assignment = self.data_base.get_assignment_details()
        else:
            assignment = self.data_base.get_assignment_details_by_course(course_id)

        if not assignment:
            print("No Assignment Available")
        else:
            print("Assignment Lists")
            for assignments in assignment:
                print(
                    f"ID: {assignments.assignment_id}, Title: {assignments.title}, Description: {assignments.description}, Due Date: {assignments.due_date.date()}, Type: {assignments.assignment_type}")

    def delete_assignments(self):
        assignment_id = int(input("Enter assignment Id you want to delete:"))
        if assignment_id:
            self.data_base.delete_assignments(assignment_id)
        else:
            print("Information Not Match!..")
