from django import forms
from django.contrib.auth.models import User
from .models import Course, Teacher, Subject, Student, Attendance, Result, Fee, Notice, Timetable

class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget_type = field.widget.__class__.__name__
            base_class = (
                "w-full px-4 py-2.5 border rounded-xl focus:outline-none focus:ring-2 transition duration-200 "
                "bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 "
                "border-zinc-300 dark:border-zinc-700 focus:ring-indigo-600 dark:focus:ring-indigo-600 focus:border-indigo-600 dark:focus:border-indigo-600"
            )
            
            if widget_type == 'CheckboxInput':
                field.widget.attrs['class'] = "rounded border-zinc-300 text-indigo-600 focus:ring-indigo-600 h-5 w-5 cursor-pointer"
            elif widget_type == 'Select':
                field.widget.attrs['class'] = base_class + " cursor-pointer"
            elif widget_type == 'DateInput':
                field.widget.attrs['class'] = base_class
                field.widget.input_type = 'date'
            elif widget_type == 'TimeInput':
                field.widget.attrs['class'] = base_class
                field.widget.input_type = 'time'
            elif widget_type == 'Textarea':
                field.widget.attrs['class'] = base_class + " resize-y min-h-[100px]"
            else:
                field.widget.attrs['class'] = base_class


class TeacherUserForm(TailwindFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Leave blank if you don't want to change the password for editing.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username


class TeacherProfileForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone', 'qualification', 'address', 'profile_pic']


class StudentForm(TailwindFormMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        required=False,
        initial="Student@123",
        help_text="Password for student portal login. Default is 'Student@123'. Leave blank to keep current password when editing."
    )

    class Meta:
        model = Student
        fields = [
            'roll_number', 'first_name', 'last_name', 'email', 
            'phone', 'gender', 'dob', 'address', 'course', 'profile_pic', 'password'
        ]
        widgets = {
            'dob': forms.DateInput(),
        }

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if Student.objects.filter(roll_number=roll_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A student with this roll number already exists.")
        return roll_number


class CourseForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']


class SubjectForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'course', 'teacher']


class AttendanceForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'status']
        widgets = {
            'date': forms.DateInput(),
        }


class ResultForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'marks_obtained', 'max_marks', 'grade', 'exam_date']
        widgets = {
            'exam_date': forms.DateInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        marks = cleaned_data.get('marks_obtained')
        max_m = cleaned_data.get('max_marks')
        if marks is not None and max_m is not None:
            if marks > max_m:
                raise forms.ValidationError("Marks obtained cannot exceed maximum marks.")
        return cleaned_data


class FeeForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student', 'amount_due', 'amount_paid', 'status', 'due_date', 'payment_date']
        widgets = {
            'due_date': forms.DateInput(),
            'payment_date': forms.DateInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        due = cleaned_data.get('amount_due')
        paid = cleaned_data.get('amount_paid')
        status = cleaned_data.get('status')
        
        if due is not None and paid is not None:
            if paid > due:
                raise forms.ValidationError("Amount paid cannot exceed amount due.")
            
            # Auto update status based on payment if it's set to pending but paid
            if paid == due and status != 'Paid':
                cleaned_data['status'] = 'Paid'
            elif paid > 0 and paid < due and status != 'Partial':
                cleaned_data['status'] = 'Partial'
            elif paid == 0 and status != 'Pending':
                cleaned_data['status'] = 'Pending'
                
        return cleaned_data


class NoticeForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'subject']


class TimetableForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['course', 'subject', 'day', 'start_time', 'end_time', 'room_number']
        widgets = {
            'start_time': forms.TimeInput(),
            'end_time': forms.TimeInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and start >= end:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data


from django.contrib.auth.forms import PasswordChangeForm

class CampusPasswordChangeForm(TailwindFormMixin, PasswordChangeForm):
    pass

