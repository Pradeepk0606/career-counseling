from itertools import groupby

from django.contrib import messages
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AccessForm
from .models import AssessmentScore, Discipline, Student, Subject


def home(request):
    """
    View function for the home page.

    Handles access form submission, validation, and redirection.
    """
    if request.method == "POST":
        form = AccessForm(request.POST)
        if form.is_valid():
            entry_code = form.cleaned_data.get("entry_code")
            request.session["entry_code"] = entry_code
            messages.success(request, "You've been granted access to your Dashboard")
            return redirect("assessment")
        else:
            messages.warning(request, "Invalid access code. Please crosscheck and try again")
    else:
        form = AccessForm()

    template = "home.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@require_POST
def end_session(request):
    """
    View function for ending a user's session.

    Deletes the 'entry_code' session variable if it exists
    and displays a success message.
    """
    if "entry_code" in request.session:
        del request.session["entry_code"]

    messages.success(request, "Your session has ended. See you next time.")
    return redirect("home")


def assessment(request):
    """
    View function for the assessment page.

    Retrieves assessment scores and calculates various statistics for the student.
    """
    entry_code = request.session.get("entry_code")
    if not entry_code:
        messages.warning(request, "Please enter an access code to view the dashboard.")
        return redirect("home")

    student = get_object_or_404(Student, entry_code=entry_code)

    student_assessment_scores = (
        AssessmentScore.objects.filter(student=student)
        .select_related("grade_level", "session_term", "subject", "subject__subject_field")
        .order_by("grade_level", "session_term")
    )

    # Group assessment scores by grade level and subject
    assessment_scores_by_grade_subject = {}
    for key, group in groupby(student_assessment_scores, key=lambda x: (x.grade_level, x.subject)):
        grade_level, subject = key
        assessment_scores_by_grade_subject.setdefault(grade_level, {}).setdefault(subject, []).extend(group)

    # Calculate overall subject totals
    subject_totals = (
        student_assessment_scores.values("subject__name")
        .annotate(total_score=Sum("total_score"))
        .order_by("-total_score", "subject__name")
    )

    # Highest performing subject
    highest_subject = None
    if subject_totals.exists():
        highest_subject = subject_totals.first()
        try:
            subj_obj = Subject.objects.get(name=highest_subject["subject__name"])
            highest_subject["subject_field"] = subj_obj.subject_field
        except Subject.DoesNotExist:
            highest_subject["subject_field"] = None

    # Calculate average score for each subject across terms/grades
    subject_average_scores = (
        student_assessment_scores.values("subject__name")
        .annotate(avg_total_score=Avg("total_score"))
        .order_by("subject__name")
    )

    # List top 3 subjects based on highest scores (excluding "General" subjects)
    top_subjects = (
        student_assessment_scores.exclude(subject__subject_field__name="General")
        .values("subject__name")
        .annotate(total_score=Sum("total_score"))
        .order_by("-total_score")[:3]
    )

    # Determine recommended career field based on top subjects
    subject_fields_of_top_subjects = []
    for subj in top_subjects:
        try:
            subj_obj = Subject.objects.get(name=subj["subject__name"])
            if subj_obj.subject_field:
                subject_fields_of_top_subjects.append(subj_obj.subject_field)
        except Subject.DoesNotExist:
            pass

    most_common_subject_field = None
    related_disciplines = Discipline.objects.none()
    if subject_fields_of_top_subjects:
        most_common_subject_field = max(set(subject_fields_of_top_subjects), key=subject_fields_of_top_subjects.count)
        related_disciplines = Discipline.objects.filter(subject_field=most_common_subject_field)

    template = "assessment.html"
    context = {
        "student": student,
        "assessment_scores_by_grade_subject": assessment_scores_by_grade_subject,
        "subject_totals": subject_totals,
        "highest_subject": highest_subject,
        "subject_average_scores": subject_average_scores,
        "top_subjects": top_subjects,
        "most_common_subject_field": most_common_subject_field,
        "related_disciplines": related_disciplines,
    }

    return render(request, template, context)

