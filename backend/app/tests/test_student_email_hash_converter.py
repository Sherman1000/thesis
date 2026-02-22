from django.test import TransactionTestCase

from app.entities.converters import StudentEmailHashConverter
from app.tests.fake_student_factory import FakeStudentFactory


class StudentEmailHashConverterTest(TransactionTestCase):
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

    def test_converter_returns_expected_hash_from_email(self):
        hashed_email = StudentEmailHashConverter(self.student_factory.student_registry()).hash_for('germandesousa@gmail.com')
        self.assertEqual(hashed_email, self._hashed_test_email())

    def test_converter_returns_expected_email_from_hash(self):
        converter = StudentEmailHashConverter(self.student_factory.student_registry())
        email = converter.recover_email_from(converter.hash_for(email='germandesousa@gmail.com'))
        self.assertEqual(email, 'germandesousa@gmail.com')

    def _hashed_test_email(self):
        return 'f6503129f3cde4f161991289e1a9fb5c'


