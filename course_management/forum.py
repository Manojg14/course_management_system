#forum.py

def get_db_manager(self):
    from database.database_mg import DataBasemanagement
    return DataBasemanagement()


class Forum:

    def __init__(self, forum_id = None,course_id = None, sender_role = None, sender_id = None, message = None, reply_to = None):
        self.forum_id = forum_id
        self.course_id = course_id
        self.sender_role = sender_role
        self.sender_id = sender_id
        self.message = message
        self.reply_to = reply_to
        self.data_base = get_db_manager(self)

    def forum_display(self):
        return f"Forum Id:{self.forum_id},Course Id:{self.course_id},Sender Role:{self.sender_role},Sender Id:{self.sender_id},Message:{self.message},Reply Message:{self.reply_to}"

    def __str__(self):
        return self.forum_display()

    def add_forum_message(self):
        course_id = int(input("Enter Your Course ID: "))
        sender_role = input("Enter your role (student or staff): ")
        sender_id = int(input("Enter Your ID: "))
        message = input("Enter Your Message: ")
        forums = Forum(course_id=course_id, sender_role=sender_role, sender_id=sender_id, message=message)
        self.data_base.insert_forum_table(forums)

    def post_reply(self):
        course_id = int(input("Enter Your Course ID: "))
        sender_role = input("Enter your role (student or staff): ")
        sender_id = int(input("Enter Your ID: "))
        reply_to = int(input("Enter the Forum ID you're replying to: "))
        message = input("Enter your reply message: ")
        reply = Forum(course_id=course_id, sender_role=sender_role, sender_id=sender_id, message=message,
                      reply_to=reply_to)
        self.data_base.insert_forum_table(reply)

    def view_forum(self, course_id=None):
        if course_id is None:
            forum = self.data_base.get_forum_details()
        else:
            forum = self.data_base.get_assignment_details_by_course(course_id)

        if not forum:
            print("No Forum is Available")
        else:
            print("Forum Lists")
            for forums in forum:
                print(
                    f"Forum Id:{forums.forum_id},Course Id:{forums.course_id},Sender Role:{forums.sender_role},Sender Id:{forums.sender_id},Message:{forums.message},Reply Message:{forums.reply_to}")

    def delete_forum_details(self):
        student_id = int(input("Enter student Id you want to delete:"))
        if self.data_base.delete_forum(student_id):
            print(f"Enrollment Id {student_id} deleted successfully!..")
        else:
            print(f"Enrollment Id {student_id} not found")

