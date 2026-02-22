from datetime import datetime

from django.db import models

from app.models import Exercise, StudentRecord


class PairReviewCorrection(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='pair_review_correction',
                                    verbose_name='Ejercicio')
    reviewer = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='pair_review_corrections',
                                 verbose_name='Corrector')
    comment_for_author = models.TextField(blank=True, verbose_name='Comentario para autor')
    correction_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Entrega')

    is_anonymous_reviewer = models.BooleanField(default=True, verbose_name='Corrector Anonimo?')
    done = models.BooleanField(default=False, verbose_name='Corregido')
    published = models.BooleanField(default=False, verbose_name='Publicado')

    class Meta:
        verbose_name = 'Revisión de pares'
        verbose_name_plural = 'Revisiones de pares'

    def __str__(self):
        return f'{self.exercise} - Corregido por {self.reviewer}'

    def unit_submission(self):
        return self.exercise.unit_submission

    def exercise_unit(self):
        return self.unit_submission().unit

    def exercise_name(self):
        return self.exercise.name

    def comment_from_author(self):
        return self.unit_submission().pair_review_comment

    def exercise_solution(self):
        return self.exercise.solution_link()

    def correct(self, comment):
        self.comment_for_author = comment
        self.correction_datetime = datetime.now()
        self.done = True

    def anonymized_reviewers_email(self):
        return self.reviewer.email if not self.is_anonymous_reviewer else '-'

    def publish(self):
        self.published = True

    def unpublish(self):
        self.published = False