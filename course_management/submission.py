# submission.py

from ... course_management_system.database.database_mg import DataBasemanagement

class Submission:
    def __init__(self, submission_id = None, assignment_id = None, student_id = None, title = None, description = None, submission_date = None):
        self.submission_id = submission_id
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.title = title
        self.description = description
        self.submission_date = submission_date
        self.data_base = DataBasemanagement()

    def add_submission(self):
        submission_id = int(input("Enter Your Submission id: "))
        assignment_id = int(input("Enter Your Assignment id: "))
        student_id = int(input("Enter Your Student id: "))
        title = input("Enter your Assignment Title: ")
        description = input("Enter Your Assignment descriptions: ")
        submission_date = input("Enter Your Date of Submission (YYYY-MM-DD): ")

        submission = Submission(
            submission_id=submission_id,
            assignment_id=assignment_id,
            student_id=student_id,
            title=title,
            description=description,
            submission_date=submission_date,

        )

        self.data_base.insert_submission_table(submission)
        print("Submission added successfully.")


    def view_submission(self):
        choice = input("Enter your choice (all or coursewise): ").strip().lower()
        if choice == "all":
            rows = self.data_base.get_submission_details()
            print(rows)
        elif choice == "coursewise":
            course_id = input("Enter courses ID: ").strip()
            submissions = self.data_base.get_submission_details_by_course(course_id=course_id)
            print(
                f"Submission ID:{submissions.submission_id},Assignment ID:{submissions.assignment_id},Student ID:{submissions.student_id},Title:{submissions.title},Answer:{submissions.description},Date:{submissions.submission_date}")

        else:
            print("Invalid choice")
            return

    def delete_submission_details(self):
        student_id = int(input("Enter Student Id you want to delete the submission:"))
        if self.data_base.delete_submission(student_id):
            print(f"Student Id {student_id} Submission Data has been deleted successfully!..")
        else:
            print(f"Student Id {student_id} not found")
