from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import random

from app.models import Exercise
from rest_framework.authtoken.admin import User


class CorrectionResponses:
    def solves_exercise_choices(self):
        SOLVES = 1
        DOES_NOT_SOLVE = 2
        EMPTY = 3

        return {
            SOLVES: 'Tiene el ejercicio pedido',
            DOES_NOT_SOLVE: 'Tiene código pero no es el ejercicio pedido',
            EMPTY: 'Está vacío / No se puede abrir',
        }.items()

    def code_evaluation_grade(self):
        NOPE = 1
        A_FEW = 2
        NORMAL = 3
        GOOD = 4
        GREAT = 5

        return {
            NOPE: 'Nop!',
            A_FEW: 'Un poco',
            NORMAL: 'Normal',
            GOOD: 'Muy bien',
            GREAT: 'Genial!',
        }.items()

    def three_level_evaluation_grade(self):
        NO = 1
        SOMETIMES = 2
        YES = 3

        return {
            NO: 'No',
            SOMETIMES: 'Pocas veces',
            YES: 'Si',
        }.items()

    def five_level_number_grading(self):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

        return {
            ONE: '1',
            TWO: '2',
            THREE: '3',
            FOUR: '4',
            FIVE: '5',
        }.items()


class Correction(models.Model):
    exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE, related_name='correction',
                                    verbose_name='Ejercicio')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True},
                                 related_name='corrections', verbose_name='Corrector')
    solves_exercise = models.IntegerField(choices=CorrectionResponses().solves_exercise_choices(), null=True,
                                          verbose_name='Resuelve ejercicio')
    code_presentation = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                    choices=CorrectionResponses().five_level_number_grading(),
                                                    verbose_name='Presentación del código')
    works = models.IntegerField(choices=CorrectionResponses().three_level_evaluation_grade(), null=True,
                                verbose_name='Funciona?')
    tests = models.IntegerField(choices=CorrectionResponses().three_level_evaluation_grade(), null=True,
                                verbose_name='Tiene tests?')
    grade = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                        choices=CorrectionResponses().five_level_number_grading(),
                                        verbose_name='Puntuación')

    comment_for_author = models.TextField(blank=True, verbose_name='Comentario para autor')
    comment_for_teachers = models.TextField(blank=True, verbose_name='Comentario para docentes')
    done = models.BooleanField(default=False, verbose_name='Corregido')
    published = models.BooleanField(default=False, verbose_name='Publicado')
    correction_time_in_minutes = models.PositiveIntegerField(null=True, verbose_name='Tiene utilizado para corregir (en minutos)')

    class Meta:
        verbose_name = 'Corrección'
        verbose_name_plural = 'Correcciones'

    @classmethod
    def for_exercise(cls, exercise):
        reviewer = cls.reviewer_for(exercise)
        return cls(exercise=exercise, reviewer=reviewer)

    @classmethod
    def reviewer_for(cls, exercise):
        reviewers = list(User.objects.filter(groups__name='Correctores'))

        if cls._has_previous_version_with_assigned_reviewer(exercise):
            return cls._assigned_reviewer_for_other_version_of(exercise)

        return random.choice(reviewers)

    @classmethod
    def _has_previous_version_with_assigned_reviewer(cls, exercise):
        return cls._other_exercise_correction_versions(exercise).exists()

    @classmethod
    def _assigned_reviewer_for_other_version_of(cls, exercise):
        return Correction._other_exercise_correction_versions(exercise).first().reviewer

    @classmethod
    def _other_exercise_correction_versions(cls, exercise):
        return cls.objects.filter(exercise__unit_submission__unit=exercise.unit(),
                                  exercise__name=exercise.name,
                                  exercise__unit_submission__student_record=exercise.student_record())

    def __str__(self):
        return f'Corrección para {self.exercise}'

    def student(self):
        return self.exercise.unit_submission.student_record

    def submission_datetime(self):
        return self.exercise.unit_submission.datetime

    def exercise_unit(self):
        return self.exercise.unit_submission.unit

    def exercise_name(self):
        return self.exercise.name

    def exercise_solution(self):
        return self.exercise.solution_link()

    def self_evaluation(self):
        return self.exercise.unit_submission.self_evaluations.last()

    def exercise_self_evaluation(self):
        return self.self_evaluation().exercise_self_evaluations.filter(exercise_name=self.exercise.name).last()

    def content_learning(self):
        return self.self_evaluation().readable_content_learning()

    def exercises_autograde(self):
        return self.self_evaluation().readable_exercises_autograde()

    def dedication_in_hours(self):
        return self.self_evaluation().dedication_in_hours

    def dedication_evaluation(self):
        return self.self_evaluation().readable_dedication_evaluation()

    def self_evaluation_comment(self):
        return self.self_evaluation().comment

    def exercise_self_evaluation_grade(self):
        return self.exercise_self_evaluation().readable_grade()

    def version(self):
        return self.exercise.version()

    def publish(self):
        self.published = True

    def unpublish(self):
        self.published = False


class CodeEvaluation(models.Model):
    correction = models.OneToOneField(Correction, on_delete=models.CASCADE, related_name='correction',
                                      verbose_name='Corrección')
    clarity = models.IntegerField(choices=CorrectionResponses().code_evaluation_grade(), verbose_name='Claridad')
    declarative = models.IntegerField(choices=CorrectionResponses().code_evaluation_grade(),
                                      verbose_name='Declaratividad')
    modular = models.IntegerField(choices=CorrectionResponses().code_evaluation_grade(), verbose_name='Modular')
    reusable = models.IntegerField(choices=CorrectionResponses().code_evaluation_grade(), verbose_name='Reusable')
    python = models.IntegerField(choices=CorrectionResponses().code_evaluation_grade(), verbose_name='Python')
    commented = models.IntegerField(choices=CorrectionResponses().code_evaluation_grade(), verbose_name='Comentarios')

    class Meta:
        verbose_name = 'Evaluación del código'
        verbose_name_plural = 'Evaluaciones de código'