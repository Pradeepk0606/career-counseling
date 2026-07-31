from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from career.models import (
    AssessmentScore,
    Discipline,
    GradeLevel,
    SessionTerm,
    Student,
    Subject,
    SubjectField,
)


class AssessmentScoreInline(admin.TabularInline):
    """
    Inline admin configuration for AssessmentScore model.
    Displays AssessmentScore fields in a tabular format within StudentAdmin.
    """

    model = AssessmentScore
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Student model.
    """

    inlines = [AssessmentScoreInline]
    list_display = ["name", "entry_code", "email"]
    search_fields = ["name", "email"]

    def save_model(self, request, obj, form, change):
        """
        Override save_model method to send an email when creating a student.
        """
        if not change:
            entry_code = obj.entry_code

            subject = "Your Entry Code"
            message = f"Hello {obj.name},\n\nYour entry code for www.careercompass.com is: {entry_code}\n\nPlease keep this code safe and use it for future references.\n\nBest regards,\nYour School Team"

            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "admin@careercompass.com")
            recipient_list = [obj.email]

            send_mail(subject, message, from_email, recipient_list)

        super().save_model(request, obj, form, change)



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Subject model.
    """

    # Sets the field which should be displayed on the admin change list page
    list_display = ["name", "subject_field"]
    # Enables filtering of the Subject by their SubjectField
    list_filter = ["subject_field"]


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Discipline model.
    """

    list_display = ["name", "subject_field"]
    search_fields = ["name", "subject_field"]
    list_filter = ["subject_field"]


# Register other models with default admin configuration
admin.site.register(SubjectField)
admin.site.register(GradeLevel)
admin.site.register(SessionTerm)

# Unregister the Group model from the admin interface
admin.site.unregister(Group)
