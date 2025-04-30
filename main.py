# main.py

from admin_login.admin import AdminLogin
from staff_login.staffs import StaffLogin
from student_login.student import StudentLogin


def main_method():
    while True:
        print("\n================= WELCOME TO LOGIN SYSTEM ============================")
        print("1. Admin Login")
        print("2. Staff Login")
        print("3. Student Login")
        print("4. Exit")
        print("="*70)

        try:
            user_choice = int(input("Click Anyone Choice (1, 2, 3, 4): "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if user_choice == 1:
            admins = AdminLogin()
            admins.handle_admin()

        elif user_choice == 2:
            staffs = StaffLogin()
            staffs.handle_staff()

        elif user_choice == 3:
            students = StudentLogin()
            students.handle_student()

        elif user_choice == 4:
            print("Exiting...")
            break

        else:
            print("Enter a valid choice!")

if __name__ == "__main__":
     main_method()