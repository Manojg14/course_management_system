import pymysql

from staff_login.staffs import Staff
from student_login.student import Student

from course_management.course import Course
from course_management.assignment import Assignment
from course_management.enrollment import Enrollment
from course_management.submission import Submission
from course_management.forum import Forum


def get_admin(self):
    from admin_login.admin import Admin
    return Admin(self)

class DataBasemanagement:
    def __init__(self):
        self.cnx = pymysql.connect(host='localhost', user='root', password='admin')
        self.cursor = self.cnx.cursor()
        self.create_database()
        self.cnx.select_db("Online_Course_Management")
        self.create_admins_table()
        self.create_staff_table()
        self.create_student_table()
        self.create_courses_table()
        self.create_assignment_table()
        self.create_enrollments_table()
        self.create_submission_table()
        self.create_forum_table()
        self.create_payment_table()

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS Online_Course_Management")

    def create_admins_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_tables(
        admin_id INT PRIMARY KEY,
        admin_name VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL       
        )
        """)

    def insert_admin_table(self,admins):
        query = """
               INSERT INTO admin_tables(admin_id, admin_name, password_hash)
               VALUES (%s, %s, %s)
               """
        self.cursor.execute(query, (admins.admin_id,admins.admin_name,admins.password_hash))
        self.cnx.commit()

    def get_admin_users(self):
        self.cursor.execute("SELECT admin_id, admin_name, password_hash FROM admin_table")
        rows = self.cursor.fetchall()
        return [get_admin(*row) for row in rows]

    def delete_admin_table(self,admin_id):
        self.cursor.execute("DELETE FROM admin_table WHERE admin_id = %s",(admin_id,))
        self.cnx.commit()
        return self.cursor.rowcount > 0

    # Staff Table
    def create_staff_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff_details(
                staff_id INT PRIMARY KEY,
                staff_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone_no VARCHAR(10) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

    def insert_staff_table(self, staffs):
        query = """
        INSERT INTO staff_details (staff_id,staff_name, email, phone_no, password_hash)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (staffs.staff_id,staffs.staff_name, staffs.email, staffs.phone_no, staffs.password_hash))
        self.cnx.commit()

    def get_staff_users(self):
        self.cursor.execute("SELECT staff_id, staff_name, email, phone_no, password_hash FROM staff_details")
        rows = self.cursor.fetchall()
        return [Staff(*row) for row in rows]

    def update_staff_details(self,staff_id, staff_name=None, email=None, phone_no=None, password_hash=None):

                if staff_name:
                    sql = "UPDATE staff_details SET staff_name = %s WHERE staff_id = %s"
                    self.cursor.execute(sql, (staff_name, staff_id))
                if email:
                    sql = "UPDATE staff_details SET email = %s WHERE staff_id = %s"
                    self.cursor.execute(sql, (email, staff_id))
                if phone_no:
                    sql = "UPDATE staff_details SET phone_no = %s WHERE staff_id = %s"
                    self.cursor.execute(sql, (phone_no, staff_id))
                if password_hash:
                    sql = "UPDATE staff_details SET password_hash = %s WHERE staff_id = %s"
                    self.cursor.execute(sql, (password_hash, staff_id))
                self.cnx.commit()


    def check_staff_credentials(self, staff_id, password_hash):

        sql = "SELECT * FROM staff_details WHERE staff_id = %s AND password_hash = %s"
        self.cursor.execute(sql, (staff_id, password_hash))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None

    def delete_staff_table(self,staff_id):
        self.cursor.execute("DELETE FROM staff_details WHERE staff_id = %s",(staff_id,))
        self.cnx.commit()
        return self.cursor.rowcount > 0

    # Student Table
    def create_student_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_details(
                student_id INT PRIMARY KEY,
                student_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone_no VARCHAR(10) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

    def insert_student_table(self, students):
        query = """ 
            INSERT INTO student_details (student_id,student_name, email, phone_no, password_hash)
            VALUES (%s, %s, %s, %s, %s)
            """
        self.cursor.execute(query, (students.student_id,students.student_name, students.email, students.phone_no, students.password_hash))
        self.cnx.commit()

    def get_student_users(self):
        self.cursor.execute("SELECT student_id, student_name, email, phone_no, password_hash FROM student_details")
        rows = self.cursor.fetchall()
        return [Student(*row) for row in rows]

    def delete_student_table(self,student_id):
        self.cursor.execute("DELETE FROM student_details WHERE student_id = %s",(student_id,))
        self.cnx.commit()
        return self.cursor.rowcount > 0

    def update_student_details(self,student_id, student_name=None, email=None, phone_no=None, password_hash=None):

                if student_name:
                    sql = "UPDATE student_details SET student_name = %s WHERE student_id = %s"
                    self.cursor.execute(sql, (student_name, student_id))
                if email:
                    sql = "UPDATE student_details SET email = %s WHERE student_id = %s"
                    self.cursor.execute(sql, (email, student_id))
                if phone_no:
                    sql = "UPDATE student_details SET phone_no = %s WHERE student_id = %s"
                    self.cursor.execute(sql, (phone_no, student_id))
                if password_hash:
                    sql = "UPDATE student_details SET password_hash = %s WHERE student_id = %s"
                    self.cursor.execute(sql, (password_hash, student_id))
                self.cnx.commit()

    def check_student_credentials(self, student_id, password_hash):

        sql = "SELECT * FROM student_details WHERE student_id = %s AND password_hash = %s"
        self.cursor.execute(sql, (student_id, password_hash))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None

    def create_courses_table(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS courses_details(
                course_id INT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                max_enrollment INT NOT NULL,
                course_fee DECIMAL(10,2),
                staff_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY(staff_id) REFERENCES staff_details (staff_id) ON DELETE CASCADE
            )
        """)

    def staff_exists(self, staff_id):
        self.cursor.execute("SELECT staff_id FROM staff_details WHERE staff_id = %s", (staff_id,))
        return self.cursor.fetchone() is not None

    def insert_course_table(self, courses):
        query = """
            INSERT INTO courses_details (course_id,title, description, max_enrollment, course_fee, staff_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (courses.course_id,courses.title, courses.description, courses.max_enrollment, courses.course_fee, courses.staff_id))
        self.cnx.commit()

    def update_course_details(self, course_id, title=None, description=None, max_enrollment=None, course_fee=None, staff_id=None):

        if title is not None:
            sql = "UPDATE courses_details SET title = %s WHERE course_id = %s"
            self.cursor.execute(sql, (title, course_id))
        if description is not None:
            sql = "UPDATE courses_details SET description = %s WHERE course_id = %s"
            self.cursor.execute(sql, (description, course_id))
        if max_enrollment is not None:
            sql = "UPDATE courses_details SET max_enrollment = %s WHERE course_id = %s"
            self.cursor.execute(sql, (max_enrollment, course_id))
        if course_fee is not None:
            sql = "UPDATE courses_details SET course_fee = %s WHERE course_id = %s"
            self.cursor.execute(sql, (course_fee, course_id))
        if staff_id is not None:
            sql = "UPDATE courses_details SET staff_id = %s WHERE course_id = %s"
            self.cursor.execute(sql, (staff_id, course_id))
        self.cnx.commit()

    def search_student_course(self):
        self.cursor.execute("SELECT course_id, title, description, max_enrollment, course_fee, staff_id FROM courses_details")
        rows = self.cursor.fetchall()
        return [Course(*row) for row in rows]

    def delete_course(self,course_id):
        self.cursor.execute("DELETE FROM courses_details WHERE course_id = %s",(course_id,))
        self.cnx.commit()
        return self.cursor.rowcount > 0


    # Enrollment Table
    def create_enrollments_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments_details(
                enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                course_id INT,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES student_details(student_id) ON DELETE CASCADE,
                FOREIGN KEY(course_id) REFERENCES courses_details(course_id) ON DELETE CASCADE
            )
        """)

    def insert_enrollment_table(self, enrollments):
        query = """
            INSERT INTO enrollments_details (student_id, course_id)
            VALUES (%s, %s)
        """
        self.cursor.execute(query, (enrollments.student_id, enrollments.course_id))
        self.cnx.commit()

    def get_enrollment_details(self):
        self.cursor.execute("SELECT enrollment_id ,student_id, course_id FROM enrollments_details ")
        rows = self.cursor.fetchall()
        return [Enrollment(*row) for row in rows]

    def get_enrollment_details_by_course(self, course_id):
        self.cursor.execute(
            "SELECT enrollment_id ,student_id, course_id FROM enrollments_details WHERE course_id = %s", (course_id,))
        rows = self.cursor.fetchall()
        return [Enrollment(*row) for row in rows]

    def get_enrollment_by_student_id(self,student_id):
        self.cursor.execute("SELECT enrollment_id ,student_id, course_id FROM enrollments_details WHERE student_id = %s", (student_id,))
        rows = self.cursor.fetchall()
        return [Enrollment(*row) for row in rows]

    def get_staff_email_by_enrollment(self, student_id, course_id):
        self.cursor.execute("""
            SELECT s.email
            FROM enrollments_details e
            JOIN courses_details c ON e.course_id = c.course_id
            JOIN staff_details s ON c.staff_id = s.staff_id
            WHERE e.student_id = %s AND e.course_id = %s
        """, (student_id, course_id))

        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_enrollment(self,enrollment_id):
        self.cursor.execute("DELETE FROM enrollments_details WHERE enrollment_id = %s",(enrollment_id,))
        self.cnx.commit()
        return self.cursor.rowcount > 0



    # Assignment Table
    def create_assignment_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignment_details(
                assignment_id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT NOT NULL,
                title VARCHAR(255),
                description TEXT NOT NULL,
                due_date DATE NOT NULL,
                assignment_type ENUM('quiz','project','homework') NOT NULL,
                FOREIGN KEY(course_id) REFERENCES courses_details(course_id) ON DELETE CASCADE
            )
        """)

    def insert_assignment_table(self, assignments):
        query = """
            INSERT INTO assignment_details(course_id, title, description, due_date, assignment_type)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (assignments.course_id, assignments.title, assignments.description, assignments.due_date, assignments.assignment_type))
        self.cnx.commit()

    def get_assignment_details(self):
        self.cursor.execute("SELECT assignment_id, course_id, title, description, due_date, assignment_type")
        rows = self.cursor.fetchall()
        return [Assignment(*row) for row in rows]

    def get_assignment_details_by_course(self, course_id):
        self.cursor.execute(
            "SELECT assignment_id, course_id, title, description, due_date, assignment_type FROM assignment_details WHERE course_id = %s", (course_id,))
        rows = self.cursor.fetchall()
        return [Assignment(*row) for row in rows]

    def delete_assignments(self,assignment_id):
        self.cursor.execute("DELETE FROM assignment_details WHERE assignment_id = %s",(assignment_id,))
        self.cnx.commit()
        return self.cursor.rowcount > 0

    # Submission Table
    def create_submission_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS submission_detail (
                submission_id INT PRIMARY KEY,
                student_id INT,
                assignment_id INT,
                title VARCHAR(255),
                description TEXT,
                submission_date DATE,
                FOREIGN KEY(student_id) REFERENCES student_details(student_id) ON DELETE CASCADE,
                FOREIGN KEY(assignment_id) REFERENCES assignment_details(assignment_id) ON DELETE CASCADE
            )
        """)

    def insert_submission_table(self, submissions):
        query = """
            INSERT INTO submission_detail (student_id, assignment_id, title, description, submission_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (submissions.student_id, submissions.assignment_id, submissions.title, submissions.description, submissions.submission_date))
        self.cnx.commit()

    def get_submission_details(self):
        self.cursor.execute("SELECT student_id, assignment_id, title, description, submission_date FROM submission_detail ")
        rows = self.cursor.fetchall()
        return [Submission(*row) for row in rows]

    def get_submission_details_by_course(self, course_id):
        self.cursor.execute(
            "SELECT student_id, assignment_id, title, description, submission_date FROM submission_detail WHERE course_id = %s", (course_id,))
        rows = self.cursor.fetchall()
        return [Submission(*row) for row in rows]

    def delete_submission(self,student_id):
        self.cursor.execute("DELETE FROM submission_detail WHERE student_id = %s",(student_id,))
        self.cnx.commit()
        return self.cursor.rowcount > 0

# FORUM
    def create_forum_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS forum_details(
            forum_id INT PRIMARY KEY AUTO_INCREMENT,
            course_id INT,
            sender_role ENUM('student','staff'),
            sender_id INT,
            message TEXT,
            reply_to INT DEFAULT NULL,
            FOREIGN KEY (course_id) REFERENCES courses_details(course_id)
            )
            """)

    def insert_forum_table(self,forums):
        query ="""
               INSERT INTO forum_details (course_id, sender_role, sender_id,message, reply_to) 
               VALUES (%s, %s, %s, %s, %s)
               """
        self.cursor.execute(query,(forums.course_id,forums.sender_role,forums.sender_id,forums.message,forums.reply_to))
        self.cnx.commit()

    def get_forum_details(self):
        self.cursor.execute("SELECT forum_id, course_id, sender_role, sender_id, message, reply_to FROM forum_details")
        rows = self.cursor.fetchall()
        return [Forum(*row) for row in rows]

    def get_forum_details_by_course(self, course_id):
        query = "SELECT forum_id, course_id, sender_role, sender_id, message, reply_to FROM forum_details WHERE course_id = %s"
        self.cursor.execute(query, (course_id,))
        rows = self.cursor.fetchall()
        return [Forum(*row) for row in rows]

    def delete_forum(self, sender_id):
        self.cursor.execute("DELETE FROM forum_details WHERE sender_id = %s", (sender_id,))
        self.cnx.commit()
        return self.cursor.rowcount > 0

# Payment

    def create_payment_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments_details (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                course_id INT,
                amount_paid DECIMAL(10,2),
                pending_amount DECIMAL(10,2),
                payment_status VARCHAR(50),
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES student_details(student_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses_details(course_id) ON DELETE CASCADE
            )
        """)
        self.cnx.commit()

    def get_student_by_id(self, student_id):
        self.cursor.execute("SELECT student_id, student_name, email FROM student_details WHERE student_id = %s",(student_id,))
        result = self.cursor.fetchone()

        if result:
            return Student(student_id=result[0], student_name=result[1], email=result[2])
        return None

    def get_course_by_id(self, course_id):
        sql = "SELECT course_id, title, course_fee FROM courses_details WHERE course_id = %s"
        self.cursor.execute(sql, (course_id,))
        result = self.cursor.fetchone()
        if result:
            # Assuming Course is your class with proper attributes
            return Course(course_id=result[0], title=result[1], course_fee=result[2])
        return None

    def get_enrollment(self, student_id, course_id):
        self.cursor.execute("SELECT * FROM enrollments_details WHERE student_id = %s AND course_id = %s",(student_id, course_id))
        return self.cursor.fetchone()

    def insert_payment_history(self, student_id, course_id, amount_paid, pending_amount, payment_status):
        sql = """
            INSERT INTO payments_details (student_id, course_id, amount_paid, pending_amount, payment_status)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (student_id, course_id, amount_paid, pending_amount, payment_status))
        self.cnx.commit()

    def get_all_payments(self):
        self.cursor.execute("""
            SELECT p.payment_id, s.student_id, s.student_name, 
                   c.course_id, c.title, 
                   p.amount_paid, p.pending_amount, 
                   p.payment_status, p.payment_date
            FROM payments_details p
            JOIN student_details s ON p.student_id = s.student_id
            JOIN courses_details c ON p.course_id = c.course_id
            ORDER BY p.payment_date DESC
        """)
        return self.cursor.fetchall()

    def get_payment_by_student_and_course(self, student_id, course_id):
        self.cursor.execute("""
            SELECT * FROM payments_details WHERE student_id = %s AND course_id = %s """, (student_id, course_id))
        return self.cursor.fetchone()












