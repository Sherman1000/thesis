from django.db import models
from django.utils.html import format_html
from django.conf import settings

from app.models import UnitSubmission


class Exercise(models.Model):
    unit_submission = models.ForeignKey(UnitSubmission, on_delete=models.CASCADE, related_name='exercises',
                                        verbose_name='Entrega de Unidad')
    name = models.CharField(max_length=128, verbose_name='Nombre')
    solution = models.FileField(blank=True, upload_to='uploads/', verbose_name='Solución')

    class Meta:
        verbose_name = 'Ejercicio'
        verbose_name_plural = 'Ejercicios'

    @classmethod
    def for_unit(cls, unit):
        return cls.objects.filter(unit_submission__unit=unit)

    def __str__(self):
        return f"Ejercicio {self.name} de {self.student_record()}"

    def solution_link(self):
        if self.solution:
            return format_html(f'<a href="{self.solution.url}">{self.name} </a>')
        else:
            return "No attachment"

    solution_link.allow_tags = True

    def download_link(self):
        return f"{settings.FRONTEND_URL}{self.solution.url}"

    def student_record(self):
        return self.unit_submission.student_record

    def unit(self):
        return self.unit_submission.unit

    def delivery_date(self):
        return self.unit_submission.datetime

    def version(self):
        submissions_of_same_student = self.__class__.objects.filter(unit_submission__unit=self.unit(),
                                                                    name=self.name,
                                                                    unit_submission__student_record=self.student_record())
        total_submissions = submissions_of_same_student.count()
        submission_version = list(submissions_of_same_student).index(self) + 1
        return f'{submission_version}/{total_submissions}'