from django.test import TransactionTestCase

from app.models import StudentRecord
from app.tests.fake_student_factory import FakeStudentFactory


class RegisterUnitSubmissionCommandTest(TransactionTestCase):
    def setUp(self):
        self.student_factory = FakeStudentFactory()
        self.student_factory.build_a_fake_student(
            {
                'Email': 'germandesousa@gmail.com',
                'Nombre': 'German',
                'Apellido': 'De Sousa',
                'País': 'Argentina',
                'Provincia': 'Buenos Aires',
                'Genero': 'Masculino',
                'Tipo Documento': 'DNI',
                'Número de documento': '36425255',
                'Ciudad': 'CABA',
                'Relacion UNSAM': 'No tengo relacion con la UNSAM',
                'Estudiante Ciencia y Tecnologia UNSAM': 'No',
                'Lugar de estudio': 'UBA',
                'Maximo nivel educativo': 'Pregrado (tecnicatura)',
                'Carrera': 'Ciencias de la Computación',
                'Trabajo': 'Eryx',
                'Posicion': 'Desarrollador',
                'Nivel programacion': 4,
                'Nivel Python': 2
            }
        )

    # def test_command_creates_unit_submission(self):
    #     #FIXME: ESTO ES CUALQUIERA
    #     user_id = 1
    #     unit_submission = RegisterUnitSubmissionCommand(user_id=user_id, unit=1, exercises=[],
    #                                                     accepts_pair_review=False).execute().get_object()
    #
    #     self.assertEqual(unit_submission.student_record_id, self._student_record())
    #     self.assertEqual(unit_submission.unit, 1)
    #     self.assertEqual(unit_submission.exercises.count(), 0)
    #     self.assertFalse(unit_submission.accepts_pair_review)

    # def test_command_creates_exercises(self):
    #     exercises = [
    #         {
    #             'exercise': 'Nombre_Ejercicio 1',
    #             'file': 'uploads/'
    #
    #         }
    #     ]
    #     unit_submission = RegisterUnitSubmissionCommand(student_id=self._student_id(), unit=1, exercises=exercises,
    #                                                     accepts_pair_review=False).execute().get_object()

    # def test_command_creates_corrections_to_be_reviewed_by_a_teacher(self):
    #     exercises = [
    #         {
    #             'exercise': 'Nombre_Ejercicio 1',
    #             'file': 'uploads/'
    #
    #         }
    #     ]
    #     unit_submission = RegisterUnitSubmissionCommand(student_id=self._student_id(), unit=1, exercises=exercises,
    #                                                     accepts_pair_review=False).execute().get_object()
    #
    #     # Assertear que se crearon correcciones
    #     # Assertear que se crearon que todas estan en false de corregido
    #     # Assertear que el asignado para corregir es un admin (sacar el booleano adentro de la correccion)


    def _student_record(self):
        student = self.student_factory.student_registry().first()
        # FIX ME: REGISTRIES
        return StudentRecord.objects.get(email=student.email())







