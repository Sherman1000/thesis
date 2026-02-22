from django.contrib import admin

from django.db import models
from django_countries.fields import CountryField
from rest_framework.authtoken.admin import User

from app.constants import Gender, ProgrammingSkills
from app.models.courses.course_record import CourseRecord


class StudentJobRecord(models.Model):
    business_name = models.CharField(max_length=512, verbose_name='Nombre Empresa')
    position = models.CharField(max_length=512, verbose_name='Posición')

    class Meta:
        verbose_name = 'Trabajo'
        verbose_name_plural = 'Trabajos'

    def __str__(self):
        return f'Trabajo: {self.business_name}'


class StudentStudiesRecord(models.Model):
    university = models.CharField(max_length=512, verbose_name='Universidad')
    career = models.CharField(max_length=512, verbose_name='Carrera')
    study_level = models.CharField(max_length=512, verbose_name='Nivel de Estudio')
    programming_skills = models.IntegerField(ProgrammingSkills.choices(), null=True)
    python_skills = models.IntegerField(ProgrammingSkills.choices(), null=True)
    university_location = models.CharField(max_length=512, verbose_name='Locación universidad')

    class Meta:
        verbose_name = 'Estudio'
        verbose_name_plural = 'Estudios'

    def __str__(self):
        return f'Estudios: {self.university} - {self.career}'


class StudentRecord(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='Usuario')
    email = models.EmailField()
    name = models.CharField(max_length=64, verbose_name='Nombre')
    surname = models.CharField(max_length=64, verbose_name='Apellido')
    gender = models.IntegerField(choices=Gender.choices(), verbose_name='Género')
    country = models.CharField(max_length=128, verbose_name='País')
    state = models.CharField(max_length=256, verbose_name='Provincia')
    city = models.CharField(max_length=256, verbose_name='Ciudad')
    id_type = models.CharField(max_length=64, verbose_name='Tipo Documento')
    id_number = models.CharField(max_length=64, verbose_name='Nro Documento')
    course = models.ForeignKey(CourseRecord, on_delete=models.CASCADE, related_name='student_records',
                               verbose_name='Curso')
    studies = models.ForeignKey(StudentStudiesRecord, on_delete=models.CASCADE, related_name='studies_records',
                                verbose_name='Estudios')
    job = models.ForeignKey(StudentJobRecord, on_delete=models.CASCADE, related_name='job_records',
                            verbose_name='Trabajo')

    class Meta:
        unique_together = ('email', 'course')
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return self.email

    def is_registered(self):
        return self.user is not None

    def registration_date(self):
        registration_date = self.user.date_joined if self.user is not None else None
        return registration_date
