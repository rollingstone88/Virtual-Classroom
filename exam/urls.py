from django.urls import path

from exam import views

app_name = 'exam'

urlpatterns = [
    path('add_question/<code>/<slug>', views.AddQuestion.as_view(), name="addquestion"),
    path('questionPaper/<code>/<slug>', views.AddQuestionPaper.as_view(), name="addquestionpaper"),
    path('CreateExam/<code>/<slug>', views.CreateExam.as_view(), name="create_exam"),
    path('teacher/viewpreviousexams/<code>', views.view_previousexams_teacher, name="teacher-previous"),
    path('teacher/viewresults/<code>', views.view_results_teacher, name="teacher_view_result"),
    path('prof/viewstudents/<code>', views.view_students_teacher, name="teacher-student"),

    path('student/viewexams/<code>', views.view_exams_student, name="view_exams_student"),
    path('student/view_previous_exams/<slug>', views.student_view_previous, name="view_previous_student"),
    path('student/appear/<int:id>', views.appear_exam, name="appear_exam"),
    path('student/result/<int:id>', views.result, name="result"),
    path('student/attendance/<code>', views.view_students_attendance, name="view_students_attendance")
]
