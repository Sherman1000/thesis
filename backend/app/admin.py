import csv
from django import forms
from django.conf import settings
from django.utils import timezone

from django.contrib import admin
from django.http import HttpResponse

from app.entities.converters import StudentEmailHashConverter
from app.models import StudentRecord, StudentJobRecord, StudentStudiesRecord, CourseRecord, Exercise, UnitSubmission, Correction, CodeEvaluation, SelfEvaluation, ExerciseSelfEvaluation
from app.models.authomatic_corrections import AuthomaticCorrection
from app.models.courses.registries import PersistentCourseRegistry
from app.models.pair_review_corrections import PairReviewCorrection
from app.models.student.registries import PersistentStudentRegistry


@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    search_fields = ["name", "surname", "email"]
    list_display = ["email", "name", "surname", "esta_registrado", "fecha_de_registracion"]
    list_filter = ["course", ("user", admin.EmptyFieldListFilter)]
    change_list_template = "student_record/student_registries_changelist.html"
    actions = ['export_registration_emails']

    @admin.display(boolean=True)
    def esta_registrado(self, obj):
        return obj.is_registered()

    def fecha_de_registracion(self, obj):
        return obj.registration_date()
    fecha_de_registracion.admin_order_field = 'user__date_joined'

    def export_registration_emails(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format('student_email_hashes')
        self._write_csv(response, items=queryset)

        return response

    def _write_csv(self, response, items):
        writer = csv.writer(response)
        self._write_column_titles(writer)
        self._write_student_rows(writer, items)

    def _write_student_rows(self, writer, students):
        email_hash_converter = self._email_hash_converter()

        for student in students:
            registration_url = f"{settings.FRONTEND_URL}/signup/{email_hash_converter.hash_for(student.email)}"
            writer.writerow([student.email, registration_url])

    def _email_hash_converter(self):
        course_registry = PersistentCourseRegistry()
        student_registry = PersistentStudentRegistry(course_registry=course_registry)
        email_hash_converter = StudentEmailHashConverter(student_registry)
        return email_hash_converter

    def _write_column_titles(self, writer):
        column_names = ['email', 'codigo']
        writer.writerow(column_names)


@admin.register(StudentJobRecord)
class StudentJobRecordAdmin(admin.ModelAdmin):
    list_display = ["business_name", "position"]
    search_fields = ["business_name", "position"]


@admin.register(StudentStudiesRecord)
class StudentStudiesRecordAdmin(admin.ModelAdmin):
    list_display = ["university", "career", "study_level"]
    search_fields = ["university", "career"]
    list_filter = ["study_level"]


@admin.register(CourseRecord)
class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ["quarter", "year"]


class ExerciseInline(admin.TabularInline):
    model = Exercise
    readonly_fields = ['unit_submission']
    extra = 0
    can_delete = True

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class UnitSubmissionAdminForm(forms.ModelForm):
    """Form que incluye fecha editable (el modelo tiene datetime con auto_now_add)."""
    fecha_entrega = forms.DateTimeField(
        label='Fecha de Entrega',
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'],
    )

    class Meta:
        model = UnitSubmission
        fields = ['student_record', 'unit', 'accepts_pair_review', 'pair_review_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.datetime:
            self.initial['fecha_entrega'] = self.instance.datetime.strftime('%Y-%m-%dT%H:%M')
        elif not self.instance.pk:
            self.initial['fecha_entrega'] = timezone.now().strftime('%Y-%m-%dT%H:%M')

    def save(self, commit=True):
        obj = super().save(commit=False)
        fecha = self.cleaned_data['fecha_entrega']
        obj.datetime = fecha
        if commit:
            obj.save()  # en creación, Django sobrescribe datetime por auto_now_add
            UnitSubmission.objects.filter(pk=obj.pk).update(datetime=fecha)
        return obj


@admin.register(UnitSubmission)
class UnitSubmissionAdmin(admin.ModelAdmin):
    form = UnitSubmissionAdminForm
    search_fields = ["student_record__email"]
    list_display = ["student_record", "unit", "datetime", "accepts_pair_review"]
    list_filter = ["unit", "accepts_pair_review"]
    inlines = [ExerciseInline]
    fieldsets = [
        (None, {
            'fields': ['student_record', 'unit', 'fecha_entrega', 'accepts_pair_review', 'pair_review_comment'],
        }),
    ]


class ExerciseSelfEvaluationInline(admin.TabularInline):
    model = ExerciseSelfEvaluation
    extra = 0
    fields = ['exercise_name', 'grade']


@admin.register(SelfEvaluation)
class SelfEvaluationAdmin(admin.ModelAdmin):
    list_display = ['unit_submission', 'content_learning', 'exercises_autograde', 'dedicacion_horas', 'dedication_evaluation', 'comment_short']
    list_filter = ['unit_submission__unit', 'content_learning', 'exercises_autograde']
    search_fields = ['unit_submission__student_record__email', 'comment']
    inlines = [ExerciseSelfEvaluationInline]
    fieldsets = [
        (None, {
            'fields': ['unit_submission', 'content_learning', 'exercises_autograde', 'dedication_in_hours',
                       'dedication_evaluation', 'comment'],
        }),
    ]

    def dedicacion_horas(self, obj):
        return obj.dedication_in_hours
    dedicacion_horas.short_description = 'Dedicación (hs)'

    def comment_short(self, obj):
        return (obj.comment[:50] + '…') if len(obj.comment) > 50 else obj.comment
    comment_short.short_description = 'Comentario'


class CodeEvaluationInline(admin.TabularInline):
    model = CodeEvaluation
    can_delete = False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Correction)
class CorrectionAdmin(admin.ModelAdmin):
    search_fields = ["exercise__unit_submission__student_record__name"]
    list_display = ["exercise", "unidad_del_ejercicio", "version", "estudiante", "reviewer", "done", "published"]
    list_filter = ["reviewer", "done", "published", "exercise__unit_submission__unit", "exercise__name"]
    change_list_template = "corrections/corrections_changelist.html"
    readonly_fields = ['nombre_del_ejercicio', 'fecha_de_entrega', 'unidad_del_ejercicio', 'solucion',
                       'sobre_los_contenidos', 'sobre_los_ejercicios', 'dedicacion_en_horas', 'sobre_la_dedicacion',
                       'comentario_autoevaluacion', 'autoevaluacion_del_ejercicio']
    actions = ['publicar']

    fieldsets = [
        (None, {
            'fields': ['exercise', 'reviewer', 'fecha_de_entrega', 'done', 'published'],
        }),
        ('Auto evaluación', {
            'fields': ['sobre_los_contenidos', 'sobre_los_ejercicios', 'dedicacion_en_horas', 'sobre_la_dedicacion',
                       'comentario_autoevaluacion']
        }),
        ('Ejercicio', {
            'fields': ['unidad_del_ejercicio', 'nombre_del_ejercicio', 'autoevaluacion_del_ejercicio', 'solucion']
        }),
        ('Corrección', {
            'fields': ['solves_exercise', 'code_presentation', 'works', 'tests', 'grade', 'comment_for_author',
                       'comment_for_teachers', 'correction_time_in_minutes']
        })
    ]
    inlines = [CodeEvaluationInline]

    def estudiante(self, obj):
        return obj.student()
    estudiante.admin_order_field = 'exercise__unit_submission__student_record'

    def fecha_de_entrega(self, obj):
        return obj.submission_datetime()

    def nombre_del_ejercicio(self, obj):
        return obj.exercise_name()

    def unidad_del_ejercicio(self, obj):
        return obj.exercise_unit()
    unidad_del_ejercicio.admin_order_field = 'exercise__unit_submission__unit'

    def autoevaluacion_del_ejercicio(self, obj):
        return obj.exercise_self_evaluation_grade()

    def solucion(self, obj):
        return obj.exercise_solution()

    def sobre_los_contenidos(self, obj):
        return obj.content_learning()

    def sobre_los_ejercicios(self, obj):
        return obj.exercise_autograde()

    def dedicacion_en_horas(self, obj):
        return obj.dedication_in_hours()

    def sobre_la_dedicacion(self, obj):
        return obj.dedication_evaluation()

    def comentario_autoevaluacion(self, obj):
        return obj.self_evaluation_comment()

    def version(self, obj):
        return obj.version()

    def publicar(self, request, queryset):
        for correction in queryset:
            correction.publish()
            correction.save()


@admin.register(PairReviewCorrection)
class PairReviewCorrectionAdmin(admin.ModelAdmin):
    search_fields = ["reviewer__email", "exercise__name"]
    list_display = ["exercise", "unidad_del_ejercicio", "estudiante", "reviewer", "es_corrector_anonimo", "done",
                    "published"]
    list_filter = ["done", "published", "is_anonymous_reviewer", "exercise__unit_submission__unit", "exercise__name"]
    change_list_template = "pair_review/pair_reviews_changelist.html"

    readonly_fields = ['nombre_del_ejercicio', 'fecha_de_correccion', 'unidad_del_ejercicio', 'solucion', 'mensaje_del_autor']
    actions = ['publicar']

    fieldsets = [
        (None, {
            'fields': ['exercise', 'reviewer', 'is_anonymous_reviewer', 'done', 'published'],
        }),
        ('Info del ejercicio', {
            'fields': ['unidad_del_ejercicio', 'nombre_del_ejercicio', 'solucion', 'fecha_de_correccion'],
        }),
        ('Corrección', {
            'fields': ['mensaje_del_autor', 'comment_for_author'],
        }),
    ]

    def estudiante(self, obj):
        return obj.exercise.unit_submission.student_record
    estudiante.admin_order_field = 'exercise__unit_submission__student_record'

    def corrector(self, obj):
        return obj.reviewer

    def unidad_del_ejercicio(self, obj):
        return obj.exercise_unit()
    unidad_del_ejercicio.admin_order_field = 'exercise__unit_submission__unit'

    def solucion(self, obj):
        return obj.exercise_solution()

    def nombre_del_ejercicio(self, obj):
        return obj.exercise_name()

    def fecha_de_correccion(self, obj):
        return obj.correction_datetime

    def mensaje_del_corrector(self, obj):
        return obj.comment_for_author

    def mensaje_del_autor(self, obj):
        return obj.comment_from_author()

    def es_corrector_anonimo(self, obj):
        return obj.is_anonymous_reviewer
    es_corrector_anonimo.boolean = True
    es_corrector_anonimo.admin_order_field = 'is_anonymous_reviewer'

    def publicar(self, request, queryset):
        for pair_review_correction in queryset:
            pair_review_correction.publish()
            pair_review_correction.save()


@admin.register(AuthomaticCorrection)
class AuthomaticCorrectionAdmin(admin.ModelAdmin):
    search_fields = ["exercise__unit_submission__student_record__name"]
    list_display = ["exercise", "correction_datetime", "published"]
    list_filter = ["exercise__unit_submission__unit", "published", "exercise__name"]
    change_list_template = "authomatic_corrections/corrections_changelist.html"
    actions = ['publicar']

    def publicar(self, request, queryset):
        for authomatic_correction in queryset:
            authomatic_correction.publish()
            authomatic_correction.save()