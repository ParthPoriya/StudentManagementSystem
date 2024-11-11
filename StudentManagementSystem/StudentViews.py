from django.shortcuts import render,redirect
from app.models import Student_Notification,Student,Student_Feedback,Student_leave,Subject,Attendance,Attendance_Report,StudentResult
from django.contrib import messages

def HOME(request):
    return render(request,'Student/home.html')

def STUDENT_NOTIFICATION(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        notification = Student_Notification.objects.filter(student_id = student_id)

        context = {
            'notification':notification
        }
        return render(request,'Student/notification.html',context)

def STUDENT_NOTIFICATION_MARK_AS_DONE(request,status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')

def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin = request.user.id)
    feedback_histroy = Student_Feedback.objects.filter(student_id = student_id)

    context = {
        'feedback_histroy':feedback_histroy
    }
    return render(request,'Student/feedback.html',context)

def STUDENT_FEEDBACK_SAVE(request):
    if request.method == 'POST':
        student_id = Student.objects.get(admin = request.user.id)
        feedback  = request.POST.get("feedback")
        feedbacks = Student_Feedback(
            student_id = student_id,
            feedback = feedback,
            feedback_reply = ""
        )

        feedbacks.save()    
        return redirect('student_feedback')
    
def STUDENT_LEAVE(request):
    student = Student.objects.get(admin = request.user.id)
    student_leave_histroy = Student_leave.objects.filter(student_id = student)
    context = {
        'student_leave_histroy':student_leave_histroy
    }
    return render(request,'Student/apply_leave.html',context)

def STUDENT_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")

        student_id = Student.objects.get(admin = request.user.id)
        student_leave = Student_leave(
            student_id = student_id,
            data = leave_date,
            message = leave_message
        )
        student_leave.save()
        messages.success(request,'Leave Successfully Sent')
        return redirect('student_leave')


def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(course = student.course_id)
    action = request.GET.get('action')

    get_subject = None
    attendance_report = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id = subject_id)
            attendance_report = Attendance_Report.objects.filter(student_id = student,attendance_id__subject_id = subject_id)



    context = {
        'subjects':subjects,
        'action':action,
        'get_subject':get_subject,
        'attendance_report':attendance_report
    }
    return render(request,'Student/view_attendance.html',context)

def VIEW_RESULT(request):
    student = Student.objects.get(admin = request.user.id)
    result = StudentResult.objects.filter(student_id = student)

    for i in result:
        assignment_mark = i.assignment_mark
        exam_mark = i.exam_mark

        mark = assignment_mark + exam_mark


    context = {
        'result':result,
        'mark':mark
    }
    return render(request,'Student/view_result.html',context)