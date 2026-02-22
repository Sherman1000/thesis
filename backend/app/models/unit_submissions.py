from django.db import models

from app.models import StudentRecord


class UnitSubmission(models.Model):
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, verbose_name='Estudiante')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Entrega')
    unit = models.IntegerField(verbose_name='Unidad')
    accepts_pair_review = models.BooleanField(verbose_name='Acepta Revisión entre Pares')
    pair_review_comment = models.TextField(blank=True, verbose_name='Comentario Revisión entre Pares')

    class Meta:
        verbose_name = 'Entrega de Unidad'
        verbose_name_plural = 'Entregas de Unidades'

    def __str__(self):
        return f'{self.student_record}: Unidad {self.unit}'