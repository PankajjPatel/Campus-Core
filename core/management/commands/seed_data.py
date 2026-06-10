import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Course, Teacher, Subject, Student, Attendance, Result, Fee, Notice, Timetable

class Command(BaseCommand):
    help = "Seeds the database with administrative and sample academic data."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Starting database seeding..."))

        # 1. Setup default Admin account
        admin_username = "_pankaj_09"
        admin_password = "Pankaj@123"
        admin_email = "admin@campuscore.com"

        if not User.objects.filter(username=admin_username).exists():
            admin_user = User.objects.create_superuser(
                username=admin_username,
                password=admin_password,
                email=admin_email,
                first_name="Pankaj",
                last_name="Core"
            )
            self.stdout.write(self.style.SUCCESS(f"Admin user '@{admin_username}' created successfully."))
        else:
            admin_user = User.objects.get(username=admin_username)
            self.stdout.write(self.style.WARNING(f"Admin user '@{admin_username}' already exists. Skipping."))

        # Clear existing sample data to prevent duplicate unique key violations
        self.stdout.write("Clearing existing data...")
        Notice.objects.all().delete()
        Timetable.objects.all().delete()
        Result.objects.all().delete()
        Attendance.objects.all().delete()
        Fee.objects.all().delete()
        Student.objects.all().delete()
        Subject.objects.all().delete()
        # Delete user-linked teachers and their django users
        Teacher.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        Course.objects.all().delete()

        # 2. Create Courses
        self.stdout.write("Creating courses...")
        c_cse = Course.objects.create(name="B.Tech Computer Science", code="CSE", description="Bachelor of Technology in Computer Science & Engineering.")
        c_math = Course.objects.create(name="B.Sc Mathematics", code="MATH", description="Bachelor of Science in Mathematics and Physics.")
        c_bba = Course.objects.create(name="Bachelor of Business Administration", code="BBA", description="Management, corporate strategies, and business analytics.")

        # 3. Create Teachers
        self.stdout.write("Creating faculty accounts...")
        # Teacher 1
        u_amit = User.objects.create_user(username="amit_teacher", password="Teacher@123", first_name="Amit", last_name="Sharma", email="amit@campuscore.com")
        t_amit = Teacher.objects.create(user=u_amit, phone="9876543210", qualification="Ph.D. in Computer Science", address="Block B, Room 304")
        
        # Teacher 2
        u_priya = User.objects.create_user(username="priya_teacher", password="Teacher@123", first_name="Priya", last_name="Verma", email="priya@campuscore.com")
        t_priya = Teacher.objects.create(user=u_priya, phone="9876543211", qualification="M.Sc. in Mathematics", address="Block A, Room 102")

        # 4. Create Subjects
        self.stdout.write("Creating subjects...")
        s_python = Subject.objects.create(name="Programming in Python", code="CSE-101", course=c_cse, teacher=t_amit)
        s_dsa = Subject.objects.create(name="Data Structures & Algorithms", code="CSE-201", course=c_cse, teacher=t_amit)
        s_discrete = Subject.objects.create(name="Discrete Mathematics", code="MTH-101", course=c_math, teacher=t_priya)
        s_calculus = Subject.objects.create(name="Calculus & Analysis", code="MTH-201", course=c_math, teacher=t_priya)
        s_finance = Subject.objects.create(name="Financial Accounting", code="BBA-101", course=c_bba, teacher=None) # Unassigned subject

        # 5. Create Students
        self.stdout.write("Registering students...")
        u_rahul = User.objects.create_user(username="CSE001", password="Student@123", first_name="Rahul", last_name="Kumar", email="rahul@gmail.com")
        st_rahul = Student.objects.create(user=u_rahul, roll_number="CSE001", first_name="Rahul", last_name="Kumar", email="rahul@gmail.com", phone="9898989801", gender="Male", dob=datetime.date(2005, 4, 12), address="Hostel 3, Room 45", course=c_cse)
        
        u_sneha = User.objects.create_user(username="CSE002", password="Student@123", first_name="Sneha", last_name="Patel", email="sneha@gmail.com")
        st_sneha = Student.objects.create(user=u_sneha, roll_number="CSE002", first_name="Sneha", last_name="Patel", email="sneha@gmail.com", phone="9898989802", gender="Female", dob=datetime.date(2005, 8, 20), address="Sector 12, Naya Raipur", course=c_cse)
        
        u_aakash = User.objects.create_user(username="MTH001", password="Student@123", first_name="Aakash", last_name="Gupta", email="aakash@gmail.com")
        st_aakash = Student.objects.create(user=u_aakash, roll_number="MTH001", first_name="Aakash", last_name="Gupta", email="aakash@gmail.com", phone="9898989803", gender="Male", dob=datetime.date(2005, 11, 5), address="Civil Lines, Bilaspur", course=c_math)

        # 6. Seed Daily Attendance
        self.stdout.write("Seeding attendance histories...")
        today = datetime.date.today()
        # Seed last 5 days
        for day_offset in range(5):
            date_val = today - datetime.timedelta(days=day_offset)
            # Skip Sundays
            if date_val.weekday() == 6:
                continue
            # CSE students attendance in CSE-101
            Attendance.objects.create(student=st_rahul, subject=s_python, date=date_val, status="Present", marked_by=u_amit)
            Attendance.objects.create(student=st_sneha, subject=s_python, date=date_val, status="Present" if day_offset % 2 == 0 else "Absent", marked_by=u_amit)
            # Math students attendance in MTH-101
            Attendance.objects.create(student=st_aakash, subject=s_discrete, date=date_val, status="Present", marked_by=u_priya)

        # 7. Seed Exam Results
        self.stdout.write("Seeding academic result scores...")
        Result.objects.create(student=st_rahul, subject=s_python, marks_obtained=88.50, max_marks=100.00, grade="A", exam_date=today - datetime.timedelta(days=10), created_by=u_amit)
        Result.objects.create(student=st_sneha, subject=s_python, marks_obtained=94.00, max_marks=100.00, grade="A+", exam_date=today - datetime.timedelta(days=10), created_by=u_amit)
        Result.objects.create(student=st_aakash, subject=s_discrete, marks_obtained=76.00, max_marks=100.00, grade="B", exam_date=today - datetime.timedelta(days=12), created_by=u_priya)

        # 8. Seed Fees Invoices
        self.stdout.write("Seeding fee collections...")
        Fee.objects.create(student=st_rahul, amount_due=45000.00, amount_paid=45000.00, status="Paid", due_date=today + datetime.timedelta(days=30), payment_date=today - datetime.timedelta(days=15))
        Fee.objects.create(student=st_sneha, amount_due=45000.00, amount_paid=20000.00, status="Partial", due_date=today + datetime.timedelta(days=30), payment_date=today - datetime.timedelta(days=2))
        Fee.objects.create(student=st_aakash, amount_due=35000.00, amount_paid=0.00, status="Pending", due_date=today + datetime.timedelta(days=20))

        # 9. Seed Timetable schedules
        self.stdout.write("Scheduling timetable slots...")
        Timetable.objects.create(course=c_cse, subject=s_python, day="Monday", start_time=datetime.time(9, 0), end_time=datetime.time(10, 30), room_number="B-304")
        Timetable.objects.create(course=c_cse, subject=s_dsa, day="Wednesday", start_time=datetime.time(11, 0), end_time=datetime.time(12, 30), room_number="B-304")
        Timetable.objects.create(course=c_math, subject=s_discrete, day="Tuesday", start_time=datetime.time(10, 0), end_time=datetime.time(11, 30), room_number="A-102")
        Timetable.objects.create(course=c_math, subject=s_calculus, day="Thursday", start_time=datetime.time(14, 0), end_time=datetime.time(15, 30), room_number="A-102")

        # 10. Seed Notices Bulletin
        self.stdout.write("Publishing bulletins...")
        Notice.objects.create(title="Mid-Term Exams Scheduling", content="The academic mid-term exams will begin from the first week of next month. Timetables will be uploaded by respective subject teachers soon.", created_by=admin_user)
        Notice.objects.create(title="Annual Cultural Registration", content="Registrations for the Annual Cultural festival 'CampusFest 2026' are now open. Forms can be collected from the student council wing.", created_by=admin_user)
        Notice.objects.create(title="Python Project Submission Deadline", content="Please submit your programming assignments on programming concepts by Friday evening.", subject=s_python, created_by=u_amit)

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
