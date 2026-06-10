from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Course, Teacher, Subject, Student, Attendance, Result, Fee, Notice, Timetable

class Command(BaseCommand):
    help = "Clears all sample/dummy academic data from the database, leaving superusers intact."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Wiping all sample/dummy data from database..."))

        try:
            # Delete models dependent on Core models
            Notice.objects.all().delete()
            self.stdout.write("Deleted all Announcements.")

            Timetable.objects.all().delete()
            self.stdout.write("Deleted all Timetable entries.")

            Result.objects.all().delete()
            self.stdout.write("Deleted all Student Results/Grades.")

            Attendance.objects.all().delete()
            self.stdout.write("Deleted all Student Attendance records.")

            Fee.objects.all().delete()
            self.stdout.write("Deleted all Fee invoices.")

            Student.objects.all().delete()
            self.stdout.write("Deleted all Students.")

            Subject.objects.all().delete()
            self.stdout.write("Deleted all Subjects.")

            Teacher.objects.all().delete()
            self.stdout.write("Deleted all Teachers.")

            # Delete all non-superuser django users (these represent teacher logins)
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write("Deleted all teacher user accounts.")

            Course.objects.all().delete()
            self.stdout.write("Deleted all Courses.")

            self.stdout.write(self.style.SUCCESS("Database reset successfully! All dummy records deleted. Superuser admin account remains intact."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred while clearing database: {str(e)}"))
