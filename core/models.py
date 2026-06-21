import datetime
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """
    Represents an academic course (e.g. B.Tech Computer Science, B.Sc Mathematics)
    offered by the institution. Contains associated subjects and syllabus.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Teacher(models.Model):
    """
    Represents a faculty member profile, linked to a Django User account.
    Teachers are assigned to subjects, take attendance, and award marks.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, default='')
    qualification = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='teachers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return self.full_name


class Subject(models.Model):
    """
    Represents a subject or module (e.g. Data Structures, Database Systems)
    taught under a Course by a specific Teacher.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.course.code}"


class Student(models.Model):
    """
    Represents a student enrolled in the institution. Linked to their roll number.
    Contains basic demographic details and link to their optional Django User login.
    """
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    roll_number = models.CharField(max_length=50, unique=True, blank=True)
    admission_year = models.IntegerField(default=datetime.date.today().year)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    address = models.TextField(blank=True, default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    profile_pic = models.ImageField(upload_to='students/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def generate_next_roll_number(cls, course, admission_year):
        if not course:
            raise ValueError("Course must be specified to generate a roll number.")
        if not admission_year:
            admission_year = datetime.date.today().year
            
        college_code = "0975"
        dept_code = course.code.upper().strip()
        mapping = {
            'CSE': 'CS',
            'CS': 'CS',
            'ME': 'ME',
            'MECH': 'ME',
            'CE': 'CE',
            'CIVIL': 'CE',
            'EE': 'EE',
            'ELECTRICAL': 'EE',
            'EC': 'EC',
            'ECE': 'EC',
            'IT': 'IT',
            'AI': 'AI',
            'AIDS': 'AI',
        }
        dept_code = mapping.get(dept_code, dept_code[:2])
        year_str = str(admission_year)[-2:]
        prefix = f"{college_code}{dept_code}{year_str}"
        
        siblings = cls.objects.filter(roll_number__startswith=prefix)
        max_serial = 1000
        for sibling in siblings:
            roll = sibling.roll_number
            serial_part = roll[len(prefix):]
            if serial_part.isdigit():
                val = int(serial_part)
                if val > max_serial:
                    max_serial = val
                    
        next_serial = max_serial + 1
        
        # Ensure uniqueness
        while True:
            candidate = f"{prefix}{next_serial}"
            if not cls.objects.filter(roll_number=candidate).exists():
                return candidate
            next_serial += 1

    def save(self, *args, **kwargs):
        if not self.roll_number:
            self.roll_number = Student.generate_next_roll_number(self.course, self.admission_year)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_attendances')

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name} - {self.date}: {self.status}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    grade = models.CharField(max_length=5)
    exam_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_results')

    class Meta:
        unique_together = ('student', 'subject', 'exam_date')

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name}: {self.marks_obtained}/{self.max_marks} ({self.grade})"


class Fee(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Partial', 'Partial')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)

    @property
    def remaining_amount(self):
        return self.amount_due - self.amount_paid

    def __str__(self):
        return f"Fee for {self.student.full_name} - Due: {self.amount_due} - Status: {self.status}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notices', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday')
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable_slots')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_slots')
    day = models.CharField(max_length=15, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20)

    class Meta:
        unique_together = ('course', 'day', 'start_time', 'room_number')

    def __str__(self):
        return f"{self.course.code} - {self.subject.name} ({self.day} {self.start_time}-{self.end_time})"
