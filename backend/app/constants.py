# FIXME: ESTO ES MUY RARO. REFACTORIZAR
class Gender:
    # FIXME OMG THIS IS SO UGLY
    @classmethod
    def choices(cls):
        MALE = 1
        FEMALE = 2
        OTHER = 3

        return [(MALE, 'Male'), (FEMALE, 'Female'), (OTHER, 'Other')]

    @classmethod
    def id_for(cls, gender):
        # FIXME: HAY QUE UNIFICAR STRINGS POR ACAAAA
        return {
            'Masculino': 1,
            'Femenino': 2,
            'Otros': 3
        }[gender]

    @classmethod
    def description_for(cls, gender):
        MALE = 1
        FEMALE = 2
        OTHER = 3

        return {
            MALE: 'Masculino',
            FEMALE: 'Femenino',
            OTHER: 'Otros'
        }[gender]


class StudyLevel:
    @classmethod
    def choices(cls):
        PREGRADO = 1
        GRADO = 2
        POSGRADO = 3
        POSDOC = 4
        # TODO: ES MEDIO RARO EL INVESTIGADOR ACA. ES UN STUDY LEVEL? Q TRATAN DE REPRESENTAR?
        RESEARCHER = 5
        OTHER = 6

        return [(PREGRADO, 'Pregrado'), (GRADO, 'Grado'), (POSGRADO, 'Posgrado'), (POSDOC, 'Posdoc'),
                (RESEARCHER, 'Researcher'), (OTHER, 'Other')]


class CarreerProgress:
    @classmethod
    def choices(cls):
        JUST_STARTING = 1
        LESS_THAN_HALF = 2
        MORE_THAN_HALF = 3
        SOON_TO_FINISH = 4
        OTHER = 5

        return [(JUST_STARTING, 'Just starting'), (LESS_THAN_HALF, 'Less than half'),
                (MORE_THAN_HALF, 'More than half'), (SOON_TO_FINISH, 'Soon to finish'), (OTHER, 'Other')]


class ProgrammingSkills:
    @classmethod
    def choices(cls):
        NONE = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4

        return [(NONE, 'None'), (LOW, 'Low'), (MEDIUM, 'Medium'), (HIGH, 'High')]


class CourseQuarter:
    # FIXME OMG THIS IS SO UGLY
    @classmethod
    def choices(cls):
        FIRST_QUARTER = 1
        SECOND_QUARTER = 2

        return [(FIRST_QUARTER, 'First Quarter'), (SECOND_QUARTER, 'Second Quarter')]

    @classmethod
    def description_for(cls, course_quarter):
        FIRST_QUARTER = 1
        SECOND_QUARTER = 2

        return {
            FIRST_QUARTER: 'First Quarter',
            SECOND_QUARTER: 'Second Quarter'
        }[course_quarter]