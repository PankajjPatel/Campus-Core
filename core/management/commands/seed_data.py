import datetime
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from core.models import Course, Teacher, Subject, Student, Attendance, Result, Fee, Notice, Timetable

class Command(BaseCommand):
    help = "Seeds the database with administrative and 500+ realistic Indian student records and histories."

    def handle(self, *args, **kwargs):
        if Student.objects.exists():
            self.stdout.write(self.style.WARNING("Student records already exist in the database. Skipping database seeding to preserve existing data."))
            return

        self.stdout.write(self.style.WARNING("Starting database seeding process..."))

        # 1. Setup default Admin account
        admin_username = "_pankaj_09"
        admin_password = "Pankaj@123"
        admin_email = "admin@campuscore.com"

        # Wrap in atomic transaction to ensure speed and consistency
        with transaction.atomic():
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
                self.stdout.write(self.style.WARNING(f"Admin user '@{admin_username}' already exists. Skipping creation."))

            # Clear existing data to prevent integrity conflicts
            self.stdout.write("Wiping existing dummy data...")
            Notice.objects.all().delete()
            Timetable.objects.all().delete()
            Result.objects.all().delete()
            Attendance.objects.all().delete()
            Fee.objects.all().delete()
            Student.objects.all().delete()
            Subject.objects.all().delete()
            Teacher.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            Course.objects.all().delete()

            # 2. Define Departments / Courses
            self.stdout.write("Seeding Courses (Departments)...")
            dept_definitions = [
                {"name": "Computer Science Engineering", "code": "CS", "desc": "Study of computers, computational systems, and software development."},
                {"name": "Mechanical Engineering", "code": "ME", "desc": "Design, analysis, manufacturing, and maintenance of mechanical systems."},
                {"name": "Civil Engineering", "code": "CE", "desc": "Design, construction, and maintenance of physical infrastructure like roads and buildings."},
                {"name": "Electrical Engineering", "code": "EE", "desc": "Study of electricity, electronics, electromagnetism, and power systems."},
                {"name": "Electronics & Communication", "code": "EC", "desc": "Design and analysis of electronic circuits and telecommunication networks."},
                {"name": "Information Technology", "code": "IT", "desc": "Management and processing of information using computers and networks."},
                {"name": "Artificial Intelligence & Data Science", "code": "AI", "desc": "Advanced study in machine learning, statistics, data analytics, and neural systems."}
            ]
            
            courses_by_code = {}
            for d in dept_definitions:
                courses_by_code[d["code"]] = Course.objects.create(
                    name=d["name"],
                    code=d["code"],
                    description=d["desc"]
                )

            # 3. Create Teachers
            self.stdout.write("Seeding Teacher and Faculty Accounts...")
            first_names_teacher = ["Rajesh", "Sanjay", "Anil", "Amit", "Kshitij", "Manoj", "Ajay", "Vikram", "Sunil", "Deepak", "Suresh", "Meena", "Ritu", "Anjali"]
            last_names_teacher = ["Patel", "Gupta", "Nair", "Sharma", "Iyer", "Verma", "Mishra", "Malhotra", "Rao", "Sen", "Choudhury", "Joshi", "Pandey", "Trivedi"]
            
            teachers = []
            for i in range(14):
                f_name = first_names_teacher[i]
                l_name = last_names_teacher[i]
                u_name = f"{f_name.lower()}_{l_name.lower()}"
                
                # Make sure username is unique
                if User.objects.filter(username=u_name).exists():
                    u_name = f"{u_name}_{i}"
                    
                u = User.objects.create_user(
                    username=u_name,
                    password="Teacher@123",
                    first_name=f_name,
                    last_name=l_name,
                    email=f"{u_name}@campuscore.com"
                )
                t = Teacher.objects.create(
                    user=u,
                    phone=f"9876543{i:03d}",
                    qualification=random.choice(["Ph.D.", "M.Tech.", "M.S."]) + f" in Engineering/Science",
                    address=f"Staff Quarter Block {random.choice(['A', 'B', 'C'])}, Room {random.randint(101, 405)}"
                )
                teachers.append(t)

            # 4. Create Subjects
            self.stdout.write("Seeding subjects and assigning teachers...")
            subject_definitions = {
                "CS": [("Programming in Python", "CS-101"), ("Data Structures & Algorithms", "CS-201"), ("Database Management Systems", "CS-301")],
                "ME": [("Thermodynamics", "ME-101"), ("Fluid Mechanics", "ME-201"), ("Machine Design", "ME-301")],
                "CE": [("Structural Analysis", "CE-101"), ("Surveying", "CE-201"), ("Geotechnical Engineering", "CE-301")],
                "EE": [("Circuit Theory", "EE-101"), ("Electrical Machines", "EE-201"), ("Power Systems", "EE-301")],
                "EC": [("Analog Electronics", "EC-101"), ("Digital Communication", "EC-201"), ("Microprocessors", "EC-301")],
                "IT": [("Web Technologies", "IT-101"), ("Software Engineering", "IT-201"), ("Computer Networks", "IT-301")],
                "AI": [("Introduction to AI", "AI-101"), ("Machine Learning", "AI-201"), ("Neural Networks & Deep Learning", "AI-301")]
            }

            subjects_by_course = {code: [] for code in courses_by_code}
            teacher_idx = 0
            for code, list_subs in subject_definitions.items():
                course = courses_by_code[code]
                for name, sub_code in list_subs:
                    t = teachers[teacher_idx % len(teachers)]
                    sub = Subject.objects.create(
                        name=name,
                        code=sub_code,
                        course=course,
                        teacher=t
                    )
                    subjects_by_course[code].append(sub)
                    teacher_idx += 1

            # 5. Generate Student Records (525 Total, 75 per Course, distributed over 3 admission years: 2024, 2025, 2026)
            self.stdout.write("Generating 525 realistic Indian student records...")
            
            # Name sources
            first_names_male = ["Aarav", "Kabir", "Vivaan", "Vihaan", "Arjun", "Aditya", "Sai", "Reyansh", "Muhammad", "Ishan", "Shaurya", "Atharva", "Krishna", "Arnav", "Akshat", "Aryan", "Dev", "Raghav", "Madhav", "Pranav", "Rohan", "Siddharth", "Yash", "Amit", "Ankit", "Karan", "Pankaj", "Rohit", "Rahul", "Manoj", "Rakesh", "Vikram", "Vijay", "Sanjay", "Ajay", "Sunil", "Anil", "Deepak", "Sandeep", "Suresh", "Rajesh", "Gaurav", "Naman", "Harsh", "Vinay", "Alok", "Aman", "Rishabh", "Mayank", "Tushar"]
            first_names_female = ["Diya", "Isha", "Ananya", "Aanya", "Pihu", "Prisha", "Ira", "Ahana", "Riya", "Aaradhya", "Saisha", "Kiara", "Myra", "Anvi", "Pari", "Sara", "Navya", "Tanvi", "Sneha", "Priya", "Pooja", "Neha", "Ritu", "Anjali", "Divya", "Aditi", "Kavita", "Sunita", "Geeta", "Preeti", "Payal", "Jyoti", "Deepa", "Shweta", "Swati", "Rashmi", "Megha", "Kiran", "Nehal", "Nisha", "Shalini", "Kriti", "Bhavna", "Kajal", "Rupali", "Garima", "Tanaya", "Pallavi", "Snehal", "Poonam"]
            last_names = ["Kumar", "Sharma", "Patel", "Gupta", "Verma", "Singh", "Joshi", "Mehta", "Rao", "Nair", "Iyer", "Iyengar", "Reddy", "Choudhury", "Das", "Banerjee", "Mukherjee", "Chatterjee", "Sen", "Ghosh", "Mishra", "Pandey", "Trivedi", "Chaturvedi", "Pathak", "Dwivedi", "Shukla", "Tiwari", "Dubey", "Yadav", "Prasad", "Shah", "Deshmukh", "Kulkarni", "Bhat", "Hegde", "Menon", "Pillai", "Gill", "Kapoor", "Bhattacharya", "Sinha", "Saxena", "Chawla", "Malhotra", "Joshi", "Agrawal", "Bansal", "Goel", "Chahal"]
            
            cities = ["Raipur", "Bilaspur", "Bhilai", "Delhi", "Mumbai", "Pune", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Jaipur", "Lucknow", "Kochi", "Indore", "Bhopal", "Nagpur", "Patna", "Ranchi", "Dehradun", "Chandigarh"]
            streets = ["Sector 5", "M.G. Road", "Park Street", "Civil Lines", "Saket", "HSR Layout", "Indiranagar", "Salt Lake", "Rajouri Garden", "Koramangala", "G.E. Road", "Link Road", "Shivaji Nagar", "Main Road", "VIP Road", "Shankar Nagar"]

            # Track unique names to avoid duplicates
            used_names = set()
            students = []
            
            years = [2024, 2025, 2026]
            
            for code, course in courses_by_code.items():
                for year in years:
                    # Generate 25 students per course-year combination (75 per course total)
                    for count in range(25):
                        # Choose gender randomly
                        gender = random.choice(["Male", "Female"])
                        if gender == "Male":
                            f_name = random.choice(first_names_male)
                        else:
                            f_name = random.choice(first_names_female)
                        
                        l_name = random.choice(last_names)
                        
                        # Handle duplicate full names
                        while f"{f_name} {l_name}" in used_names:
                            l_name = random.choice(last_names)
                            
                        used_names.add(f"{f_name} {l_name}")
                        
                        # Email
                        email_domain = random.choice(["gmail.com", "yahoo.co.in", "outlook.com", "campuscore.edu"])
                        email = f"{f_name.lower()}.{l_name.lower()}{random.randint(10, 999)}@{email_domain}"
                        
                        # Phone
                        phone = f"{random.choice(['9', '8', '7', '6'])}{''.join(random.choices('0123456789', k=9))}"
                        
                        # Address
                        address = f"{random.randint(1, 200)}, {random.choice(streets)}, {random.choice(cities)}"
                        
                        # Date of birth (18 to 22 years old)
                        dob_year = year - random.randint(18, 21)
                        dob = datetime.date(dob_year, random.randint(1, 12), random.randint(1, 28))
                        
                        # Generate the roll number
                        roll_number = Student.generate_next_roll_number(course, year)
                        
                        # Create Django user
                        username = roll_number
                        django_user = User.objects.create_user(
                            username=username,
                            email=email,
                            first_name=f_name,
                            last_name=l_name,
                            password="Student@123"
                        )
                        
                        # Create Student profile
                        student = Student.objects.create(
                            user=django_user,
                            roll_number=roll_number,
                            admission_year=year,
                            first_name=f_name,
                            last_name=l_name,
                            email=email,
                            phone=phone,
                            gender=gender,
                            dob=dob,
                            address=address,
                            course=course
                        )
                        students.append(student)

            self.stdout.write(self.style.SUCCESS(f"Successfully generated {len(students)} Student profiles and user logins."))

            # 6. Seed Daily Attendance History (Last 10 calendar days, excluding Sundays)
            self.stdout.write("Generating student attendance logs...")
            today = datetime.date.today()
            attendance_dates = []
            offset = 0
            while len(attendance_dates) < 10:
                d = today - datetime.timedelta(days=offset)
                if d.weekday() != 6: # Skip Sunday
                    attendance_dates.append(d)
                offset += 1

            attendance_records = []
            for s in students:
                course_code = s.course.code
                subjects = subjects_by_course[course_code]
                
                # Pick 2 subjects for attendance tracking for this student to keep it realistic
                student_subs = random.sample(subjects, 2)
                
                for sub in student_subs:
                    for d_val in attendance_dates:
                        # 88% chance of being Present
                        status = "Present" if random.random() < 0.88 else "Absent"
                        attendance_records.append(Attendance(
                            student=s,
                            subject=sub,
                            date=d_val,
                            status=status,
                            marked_by=sub.teacher.user if sub.teacher else admin_user
                        ))
            
            # Bulk create attendance records for maximum execution speed
            Attendance.objects.bulk_create(attendance_records, batch_size=2000)
            self.stdout.write(self.style.SUCCESS(f"Generated {Attendance.objects.count()} attendance logs."))

            # 7. Seed Exam Results / Academic Grades
            self.stdout.write("Generating student academic results...")
            results_records = []
            for s in students:
                course_code = s.course.code
                subjects = subjects_by_course[course_code]
                
                # Students have marks for all 3 subjects in their course
                for sub in subjects:
                    max_marks = 100.00
                    # Random realistic marks with average around 75
                    marks_obtained = round(random.uniform(40.0, 99.0), 2)
                    
                    pct = (marks_obtained / max_marks) * 100
                    if pct >= 90: grade = 'A+'
                    elif pct >= 80: grade = 'A'
                    elif pct >= 70: grade = 'B'
                    elif pct >= 60: grade = 'C'
                    elif pct >= 50: grade = 'D'
                    elif pct >= 40: grade = 'E'
                    else: grade = 'F'
                    
                    results_records.append(Result(
                        student=s,
                        subject=sub,
                        marks_obtained=marks_obtained,
                        max_marks=max_marks,
                        grade=grade,
                        exam_date=today - datetime.timedelta(days=15),
                        created_by=sub.teacher.user if sub.teacher else admin_user
                    ))

            Result.objects.bulk_create(results_records, batch_size=2000)
            self.stdout.write(self.style.SUCCESS(f"Generated {Result.objects.count()} student exam grade results."))

            # 8. Seed Fees Invoices
            self.stdout.write("Generating student fee collection invoices...")
            fee_records = []
            for s in students:
                amount_due = random.choice([45000.00, 50000.00, 55000.00, 60000.00])
                
                # Status distribution: 70% Paid, 20% Partial, 10% Pending
                rand_val = random.random()
                if rand_val < 0.70:
                    status = 'Paid'
                    amount_paid = amount_due
                    payment_date = today - datetime.timedelta(days=random.randint(1, 20))
                elif rand_val < 0.90:
                    status = 'Partial'
                    amount_paid = random.choice([15000.00, 20000.00, 25000.00, 30000.00])
                    payment_date = today - datetime.timedelta(days=random.randint(1, 10))
                else:
                    status = 'Pending'
                    amount_paid = 0.00
                    payment_date = None
                    
                due_date = today + datetime.timedelta(days=random.randint(15, 45))
                
                fee_records.append(Fee(
                    student=s,
                    amount_due=amount_due,
                    amount_paid=amount_paid,
                    status=status,
                    due_date=due_date,
                    payment_date=payment_date
                ))

            Fee.objects.bulk_create(fee_records, batch_size=2000)
            self.stdout.write(self.style.SUCCESS(f"Generated {Fee.objects.count()} student fees invoices."))

            # 9. Seed Timetable Slots
            self.stdout.write("Generating course timetables...")
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            for code, course in courses_by_code.items():
                subjects = subjects_by_course[code]
                for idx, sub in enumerate(subjects):
                    day = days[idx % len(days)]
                    # Create slot
                    Timetable.objects.create(
                        course=course,
                        subject=sub,
                        day=day,
                        start_time=datetime.time(9 + (idx * 2), 0),
                        end_time=datetime.time(10 + (idx * 2), 30),
                        room_number=f"{code}-{101 + idx}"
                    )

            # 10. Seed Notices Bulletin board
            self.stdout.write("Generating institutional bulletin notices...")
            Notice.objects.create(
                title="Mid-Term Examination Registrations 2026",
                content="The registrations for the upcoming mid-term examinations for all engineering streams are open. Ensure all outstanding fees are settled before collecting your hall tickets.",
                created_by=admin_user
            )
            Notice.objects.create(
                title="Annual Project Exposition 'CoreFest-26'",
                content="Get ready for CoreFest-26! Display your software and hardware models on 15th July. Register your projects with your respective subject faculty coordinators.",
                created_by=admin_user
            )
            Notice.objects.create(
                title="Academic Advisory - Course Registrations",
                content="Please verify that your registered subjects match your curriculum. Contact the academic office immediately in case of discrepancies.",
                created_by=admin_user
            )
            
            # Subject specific notices
            for code, subjects in subjects_by_course.items():
                for sub in subjects:
                    Notice.objects.create(
                        title=f"{sub.name} Assignment Announcement",
                        content=f"Important notification regarding {sub.name} project submissions. Please submit the digital copy to the coordinator portal before the weekend.",
                        subject=sub,
                        created_by=sub.teacher.user if sub.teacher else admin_user
                    )

            self.stdout.write(self.style.SUCCESS("Database seeding completed successfully! All metrics online."))
