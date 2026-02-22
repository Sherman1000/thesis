class Student:
    @classmethod
    def from_request(cls, request):
        # FIXME: ESTO ESTA RARO
        return cls(email=request['Email'], name=request['Nombre'], surname=request['Apellido'], country=request['País'],
                   state=request['Provincia'], gender=request.get('Genero', 'Otros'), course=request['course'],
                   id_type=request['Tipo Documento'], id_number=request['Número de documento'], city=request['Ciudad'],
                   studies=request['studies'], job=request['job'])

    def __init__(self, email, name, surname, country, state, city, id_type, id_number, gender, course, studies, job):
        self._email = email
        self._name = name
        self._surname = surname
        self._country = country
        self._state = state
        self._city = city
        self._id_type = id_type
        self._id_number = id_number
        self._gender = gender
        self._course = course
        self._studies = studies
        self._job = job

    def __eq__(self, other):
        return self.email() == other.email()

    def email(self):
        return self._email

    def name(self):
        return self._name

    def surname(self):
        return self._surname

    def country(self):
        return self._country

    def state(self):
        return self._state

    def city(self):
        return self._city

    def id_type(self):
        return self._id_type

    def id_number(self):
        return self._id_number

    def gender(self):
        return self._gender

    def course(self):
        return self._course

    def studies(self):
        return self._studies

    def job(self):
        return self._job


class StudentRegistrar:
    def __init__(self, student_registry, studies_registry, job_registry, course):
        self._student_registry = student_registry
        self._studies_registry = studies_registry
        self._job_registry = job_registry
        self._course = course

    def student_registry(self):
        return self._student_registry

    def course(self):
        return self._course

    def studies_registry(self):
        return self._studies_registry

    def job_registry(self):
        return self._job_registry

    def process(self, students_request):
        for student_request in students_request:
            job = self._register_job(student_request)
            studies = self._register_studies(student_request)

            student_request.update({'course': self.course(), 'studies': studies, 'job': job})
            self.student_registry().append(Student.from_request(student_request))

    def _register_studies(self, student_request):
        programming_skills = student_request['Nivel programacion'] if student_request['Nivel programacion'] else None
        python_skills = student_request['Nivel Python'] if student_request['Nivel Python'] else None

        studies = Studies(university=student_request['Lugar de estudio'], career=student_request['Carrera'],
                          study_level=student_request['Maximo nivel educativo'],
                          programming_skills=programming_skills,
                          python_skills=python_skills)
        self.studies_registry().append(studies)
        return studies

    def _register_job(self, student_request):
        job = Job(business_name=student_request['Trabajo'], position=student_request.get('Posicion', ''))
        self.job_registry().append(job)
        return job


class Studies:
    def __init__(self, university, career, study_level, programming_skills, python_skills):
        self._university = university
        self._career = career
        self._study_level = study_level
        self._programming_skills = programming_skills
        self._python_skills = python_skills

    def university(self):
        return self._university

    def career(self):
        return self._career

    def study_level(self):
        return self._study_level

    def programming_skills(self):
        return self._programming_skills

    def python_skills(self):
        return self._python_skills


class Job:
    def __init__(self, business_name, position):
        self._business_name = business_name
        self._position = position

    def business_name(self):
        return self._business_name

    def position(self):
        return self._position
