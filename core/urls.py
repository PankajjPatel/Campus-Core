from django.urls import path
from . import views

urlpatterns = [
    # Public & Auth
    path('', views.PublicPortalView.as_view(), name='public_portal'),
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('login/', views.CampusLoginView.as_view(), name='login'),
    path('logout/', views.CampusLogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardRouterView.as_view(), name='dashboard_router'),
    path('password-change/', views.CampusPasswordChangeView.as_view(), name='password_change'),

    # Admin Dashboard & General
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),

    # Admin Student CRUD
    path('admin-dashboard/students/', views.AdminStudentListView.as_view(), name='admin_student_list'),
    path('admin-dashboard/students/add/', views.AdminStudentCreateView.as_view(), name='admin_student_add'),
    path('admin-dashboard/students/<int:pk>/edit/', views.AdminStudentUpdateView.as_view(), name='admin_student_edit'),
    path('admin-dashboard/students/<int:pk>/delete/', views.AdminStudentDeleteView.as_view(), name='admin_student_delete'),

    # Admin Teacher CRUD
    path('admin-dashboard/teachers/', views.AdminTeacherListView.as_view(), name='admin_teacher_list'),
    path('admin-dashboard/teachers/add/', views.AdminTeacherCreateView.as_view(), name='admin_teacher_add'),
    path('admin-dashboard/teachers/<int:pk>/edit/', views.AdminTeacherUpdateView.as_view(), name='admin_teacher_edit'),
    path('admin-dashboard/teachers/<int:pk>/delete/', views.AdminTeacherDeleteView.as_view(), name='admin_teacher_delete'),

    # Admin Course CRUD
    path('admin-dashboard/courses/', views.AdminCourseListView.as_view(), name='admin_course_list'),
    path('admin-dashboard/courses/<int:pk>/edit/', views.AdminCourseUpdateView.as_view(), name='admin_course_edit'),
    path('admin-dashboard/courses/<int:pk>/delete/', views.AdminCourseDeleteView.as_view(), name='admin_course_delete'),

    # Admin Subject CRUD
    path('admin-dashboard/subjects/', views.AdminSubjectListView.as_view(), name='admin_subject_list'),
    path('admin-dashboard/subjects/<int:pk>/edit/', views.AdminSubjectUpdateView.as_view(), name='admin_subject_edit'),
    path('admin-dashboard/subjects/<int:pk>/delete/', views.AdminSubjectDeleteView.as_view(), name='admin_subject_delete'),

    # Admin Attendance Management
    path('admin-dashboard/attendance/', views.AdminAttendanceListView.as_view(), name='admin_attendance_list'),
    path('admin-dashboard/attendance/mark/', views.AdminAttendanceMarkView.as_view(), name='admin_attendance_mark'),

    # Admin Result Management
    path('admin-dashboard/results/', views.AdminResultListView.as_view(), name='admin_result_list'),
    path('admin-dashboard/results/add/', views.AdminResultCreateView.as_view(), name='admin_result_add'),
    path('admin-dashboard/results/<int:pk>/edit/', views.AdminResultUpdateView.as_view(), name='admin_result_edit'),
    path('admin-dashboard/results/<int:pk>/delete/', views.AdminResultDeleteView.as_view(), name='admin_result_delete'),

    # Admin Fee Management
    path('admin-dashboard/fees/', views.AdminFeeListView.as_view(), name='admin_fee_list'),
    path('admin-dashboard/fees/add/', views.AdminFeeCreateView.as_view(), name='admin_fee_add'),
    path('admin-dashboard/fees/<int:pk>/edit/', views.AdminFeeUpdateView.as_view(), name='admin_fee_edit'),
    path('admin-dashboard/fees/<int:pk>/delete/', views.AdminFeeDeleteView.as_view(), name='admin_fee_delete'),

    # Admin Timetable Management
    path('admin-dashboard/timetable/', views.AdminTimetableListView.as_view(), name='admin_timetable_list'),
    path('admin-dashboard/timetable/add/', views.AdminTimetableCreateView.as_view(), name='admin_timetable_add'),
    path('admin-dashboard/timetable/<int:pk>/edit/', views.AdminTimetableUpdateView.as_view(), name='admin_timetable_edit'),
    path('admin-dashboard/timetable/<int:pk>/delete/', views.AdminTimetableDeleteView.as_view(), name='admin_timetable_delete'),

    # Admin Notice Management
    path('admin-dashboard/notices/', views.AdminNoticeListView.as_view(), name='admin_notice_list'),
    path('admin-dashboard/notices/add/', views.AdminNoticeCreateView.as_view(), name='admin_notice_add'),
    path('admin-dashboard/notices/<int:pk>/edit/', views.AdminNoticeUpdateView.as_view(), name='admin_notice_edit'),
    path('admin-dashboard/notices/<int:pk>/delete/', views.AdminNoticeDeleteView.as_view(), name='admin_notice_delete'),

    # Teacher Dashboard
    path('teacher-dashboard/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('teacher-dashboard/subjects/', views.TeacherSubjectListView.as_view(), name='teacher_subject_list'),
    path('teacher-dashboard/attendance/mark/<int:subject_id>/', views.TeacherAttendanceMarkView.as_view(), name='teacher_attendance_mark'),
    path('teacher-dashboard/results/manage/<int:subject_id>/', views.TeacherResultManageView.as_view(), name='teacher_result_manage'),
    path('teacher-dashboard/students/', views.TeacherStudentListView.as_view(), name='teacher_student_list'),
    path('teacher-dashboard/notices/', views.TeacherNoticeListView.as_view(), name='teacher_notice_list'),
    path('teacher-dashboard/notices/add/', views.TeacherNoticeCreateView.as_view(), name='teacher_notice_add'),

    # Reports and Exports
    path('admin-dashboard/reports/', views.AdminReportsView.as_view(), name='admin_reports'),
    path('admin-dashboard/reports/students/excel/', views.export_students_excel, name='export_students_excel'),
    path('admin-dashboard/reports/teachers/excel/', views.export_teachers_excel, name='export_teachers_excel'),
    path('admin-dashboard/reports/student/<int:student_id>/pdf/', views.export_student_pdf, name='export_student_pdf'),
]
