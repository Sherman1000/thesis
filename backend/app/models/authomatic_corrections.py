from django.db import models

from app.models import Exercise


class AuthomaticCorrection(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='authomatic_correction',
                                 verbose_name='Ejercicio')
    executed_instruction = models.CharField(verbose_name='Ejecucion', max_length=2056)
    is_original = models.BooleanField(verbose_name='Es original?')
    evaluated_code = models.TextField(verbose_name='Codigo evaluado')
    correct_tests_percentage = models.FloatField(verbose_name='Porcentaje de tests correctos')
    # FIXME: Perdemos forma normal. Que hacemos aca?
    recommendations = models.TextField(verbose_name='Listado de Recomendaciones')
    errors = models.TextField(verbose_name='Listado de errores')
    worked = models.BooleanField(verbose_name='Funciona?')
    correction_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Entrega')
    published = models.BooleanField(default=False, verbose_name='Publicado')

    class Meta:
        verbose_name = 'Corrección automática'
        verbose_name_plural = 'Correcciones automáticas'

    @classmethod
    def from_request(cls, request):
        exercise_id = request['exercise_id']
        executed_instruction = request['executed_instruction']
        is_original = request['is_original'] == 'true'
        evaluated_code = request['evaluated_code']
        correct_tests_percentage = request['correct_tests_percentage']
        recommendations = request['recommendations']
        errors = request['errors']
        worked = request['worked'] == 'true'

        return cls(exercise_id=exercise_id, executed_instruction=executed_instruction, is_original=is_original,
                   evaluated_code=evaluated_code, correct_tests_percentage=correct_tests_percentage,
                   recommendations=recommendations, errors=errors, worked=worked)

    def __str__(self):
        return f"Corrección automática para {self.exercise}"

    def publish(self):
        self.published = True

    def unpublish(self):
        self.published = False
