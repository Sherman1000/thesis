from django.db import models

from app.models import Exercise, UnitSubmission


class SelfEvaluationResponses:
    def content_learning_responses(self):
        NONE = 1
        HARD_TO_UNDERSTAND = 2
        ALMOST_EVERYTHING = 3
        EVERYTHING = 4

        return {
            NONE: 'No entendi casi nada / no la leí',
            HARD_TO_UNDERSTAND: 'Me costó entender',
            ALMOST_EVERYTHING: 'Entendí casi todo',
            EVERYTHING: 'La segui sin problemas'
        }

    def exercises_autograde_responses(self):
        BAD = 1
        HARD = 2
        GOOD = 3
        EXCELLENT = 4

        return {
            BAD: 'No hice ninguno',
            HARD: 'Me costaron mucho trabajo',
            GOOD: 'En general me salieron bien',
            EXCELLENT: 'Los hice sin problemas'
        }

    def dedication_evaluation_responses(self):
        OK = 1
        TOO_MUCH = 2
        TOO_LITTLE = 3

        return {
            OK: 'Me pareció adecuado',
            TOO_MUCH: 'Me llevó más tiempo del que me hubiera gustado dedicarle',
            TOO_LITTLE: 'Le podría haber dedicado más tiempo. Me sobró tiempo',
        }

    def exercises_grade_responses(self):
        HAVE_NOT_TRIED = 1
        DOES_NOT_UNDERSTAND = 2
        COULD_NOT_DO_IT = 3
        NOT_SURE = 4
        PARTIALLY_DID_IT = 5
        DID_IT = 6

        return {
            HAVE_NOT_TRIED: 'No lo intenté',
            DOES_NOT_UNDERSTAND: 'No entendí la consigna',
            COULD_NOT_DO_IT: 'No me salió',
            NOT_SURE: 'No estoy seguro/a',
            PARTIALLY_DID_IT: 'Me salió parcialmente',
            DID_IT: 'Me salió bien'
        }

    def content_learning_choices(self):
        return self.content_learning_responses().items()

    def exercises_autograde_choices(self):
        return self.exercises_autograde_responses().items()

    def dedication_evaluation_choices(self):
        return self.dedication_evaluation_responses().items()

    def exercises_grade_choices(self):
        return self.exercises_grade_responses().items()


class SelfEvaluation(models.Model):
    unit_submission = models.ForeignKey(UnitSubmission, on_delete=models.CASCADE, related_name='self_evaluations',
                                        verbose_name='Entrega de Unidad')
    content_learning = models.IntegerField(choices=SelfEvaluationResponses().content_learning_choices(),
                                           verbose_name='Sobre los contenidos')
    exercises_autograde = models.IntegerField(choices=SelfEvaluationResponses().exercises_autograde_choices(),
                                              verbose_name='Sobre los ejercicios')
    dedication_in_hours = models.IntegerField(default=0, verbose_name='Dedicación en horas')
    dedication_evaluation = models.IntegerField(choices=SelfEvaluationResponses().dedication_evaluation_choices(),
                                                verbose_name='Sobre la dedicación')
    comment = models.TextField(verbose_name='Comentario')

    class Meta:
        verbose_name = 'Autoevaluación'
        verbose_name_plural = 'Autoevaluaciones'

    def __str__(self):
        return f'Autoevaluación: {self.unit_submission}'

    # FIXME: NOMBRE MALISIMO
    def readable_content_learning(self):
        return SelfEvaluationResponses().content_learning_responses()[self.content_learning]

    def readable_exercises_autograde(self):
        return SelfEvaluationResponses().exercises_autograde_responses()[self.exercises_autograde]

    def readable_dedication_evaluation(self):
        return SelfEvaluationResponses().dedication_evaluation_responses()[self.dedication_evaluation]


class ExerciseSelfEvaluation(models.Model):
    self_evaluation = models.ForeignKey(SelfEvaluation, on_delete=models.CASCADE, 
                                        related_name='exercise_self_evaluations', verbose_name='Autoevaluación')
    exercise_name = models.CharField(max_length=128, verbose_name='Nombre del Ejercicio')
    grade = models.IntegerField(choices=SelfEvaluationResponses().exercises_grade_choices(), verbose_name='Puntuación')

    class Meta:
        verbose_name = 'Autoevaluación de ejercicio'
        verbose_name_plural = 'Autoevaluaciones de ejercicios'

    def __str__(self):
        return f'Autoevaluación Ejercicio {self.exercise_name} de {self.self_evaluation}'

    def readable_grade(self):
        return SelfEvaluationResponses().exercises_grade_responses()[self.grade]
