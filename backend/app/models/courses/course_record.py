from django.db import models

from app.constants import CourseQuarter


class CourseRecord(models.Model):
    quarter = models.IntegerField(choices=CourseQuarter.choices(), verbose_name='Cuatrimestre')
    year = models.IntegerField(verbose_name='Año')

    class Meta:
        unique_together = ('quarter', 'year')
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return f'{CourseQuarter.description_for(self.quarter)} - {self.year}'

    @classmethod
    def current(cls):
        return cls.objects.last()
