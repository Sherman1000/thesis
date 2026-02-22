from datetime import date, datetime

from django.contrib.auth import authenticate
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token

from app.commands.base import Command
from app.commands.validators import UserExistValidator, UserIsLoggedValidator, PasswordConfirmationValidator, \
    UserIsStaffValidator, UserIsLoggedInOrIsStaffValidator
from app.entities.converters import StudentEmailHashConverter
from app.exceptions import DoesNotExistException
from app.models import StudentRecord, UnitSubmission, Exercise, Correction, SelfEvaluation, ExerciseSelfEvaluation, \
    SelfEvaluationResponses, CourseRecord
from app.models.authomatic_corrections import AuthomaticCorrection
from app.models.courses.registries import PersistentCourseRegistry
from app.models.pair_review_corrections import PairReviewCorrection
from app.models.student.registries import PersistentStudentRegistry


class ByPassCommand(Command):
    def validators(self):
        return []

    def _execute_from_successful_validation(self, result):
        pass


class IdentityCommand(Command):
    def __init__(self, arg):
        self._arg = arg

    def validators(self):
        return []

    def _execute_from_successful_validation(self, result):
        result.set_object(self._arg)


class ChainCommands(Command):
    """
    Executes one command at a time, it uses the last result as the input for the next command in the chain, and so on.
    You need to pass arguments for the first command.
    It uses shortcut execution. Check the implementation to see how arguments are passed.
    """

    def __init__(self, commands, initial_args):
        self._commands = commands
        self._initial_args = initial_args

    def validators(self):
        return []

    def _set_command_with_args(self, command, args):
        if type(args) == tuple:
            return command(*args)
        else:
            return command(args)

    def _shortcut_execution(self):
        last_result = self._set_command_with_args(command=self._commands[0], args=self._initial_args).execute()
        for command in self._commands[1:]:
            if last_result.has_errors():
                break
            result_object = last_result.get_object()
            last_result = self._set_command_with_args(command=command, args=result_object).execute()
        return last_result

    def _execute_from_successful_validation(self, result):
        execution_result = self._shortcut_execution()
        result.copy_from(another_result=execution_result)


class GetUserFromUsernameAndPasswordCommand(Command):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def validators(self):
        return []

    def _execute_from_successful_validation(self, result):
        user = authenticate(username=self._username, password=self._password)
        if user:
            result.set_object(user)
        else:
            result.add_error(f'Username or password incorrect')


class LoginCommand(Command):
    def __init__(self, user):
        self._user = user

    def validators(self):
        return []

    def _execute_from_successful_validation(self, result):
        token, _ = Token.objects.get_or_create(user=self._user)
        result.set_object({'user': self._user, 'token': token.key})


class GetUserCommand(Command):
    def __init__(self, user_id):
        self._user_id = user_id

    def validators(self):
        return [UserExistValidator(user_id=self._user_id)]

    def _execute_from_successful_validation(self, result):
        result.set_object(User.objects.get(id=self._user_id))


class LogoutCommand(Command):
    def __init__(self, user):
        self._user = user

    def validators(self):
        return [UserIsLoggedValidator(user=self._user)]

    def _execute_from_successful_validation(self, result):
        Token.objects.get(user=self._user).delete()
        result.set_object({'user': self._user})


class GetStudentegistrationStatusCommand(Command):
    def __init__(self, email_hash):
        self._email_hash = email_hash

    def email_hash(self):
        return self._email_hash

    def validators(self):
        return []

    def _execute_from_successful_validation(self, result):
        course_registry = PersistentCourseRegistry()
        student_registry = PersistentStudentRegistry(course_registry=course_registry)

        try:
            email = StudentEmailHashConverter(student_registry).recover_email_from(self.email_hash())
        except DoesNotExistException:
            result.add_error(f'Not a student registered to this quarter')
            return result

        result.set_object({
            'email': email,
            'is_registered': User.objects.filter(username=email, email=email).exists()
        })

        return result


class RegisterUserOrChangePasswordCommand(Command):
    def __init__(self, email, password, password_confirmation, email_hash):
        self._email = email
        self._password = password
        self._password_confirmation = password_confirmation
        self._email_hash = email_hash

    def validators(self):
        return [PasswordConfirmationValidator(self._password, self._password_confirmation)]

    def _execute_from_successful_validation(self, result):
        if self._is_registering():
            user = User.objects.create_user(username=self._email, email=self._email, password=self._password)
            self._add_user_to_student_record(user)
        else:
            user = User.objects.get(username=self._email, email=self._email)
            user.set_password(self._password)
            user.save()

        token, _ = Token.objects.get_or_create(user=user)
        result.set_object({'user': user, 'token': token.key})

        return result

    def _add_user_to_student_record(self, user):
        student = StudentRecord.objects.get(email=self._email)
        student.user = user
        student.save()

    def _is_registering(self):
        return not User.objects.filter(username=self._email, email=self._email).exists()


class RegisterUnitSubmissionCommand(Command):
    def __init__(self, user_id, unit, exercises, accepts_pair_review, pair_review_comment, self_evaluation):
        self._user = user_id
        self._unit = unit
        self._exercises = exercises
        self._accepts_pair_review = accepts_pair_review
        self._pair_review_comment = pair_review_comment
        self._self_evaluation = self_evaluation

    def validators(self):
        return [UserIsLoggedValidator(user=self._user)]

    def student_record(self):
        return StudentRecord.objects.get(user_id=self._user)

    def _execute_from_successful_validation(self, result):
        unit_submission = self._create_unit_submission()
        self._create_exercises(unit_submission)
        self.register_self_evaluation(unit_submission)

        result.set_object(unit_submission)
        return result

    def _create_unit_submission(self):
        unit_submission = UnitSubmission.objects.create(student_record=self.student_record(), unit=self._unit,
                                                        accepts_pair_review=self._accepts_pair_review,
                                                        pair_review_comment=self._pair_review_comment)

        return unit_submission

    def _create_exercises(self, unit_submission):
        exercises = []
        for exercise_name, solution in self._exercises:
            if self._file_is_loaded(solution):
                self._format_file_name_for_user(exercise_name, solution)
                exercise = Exercise.objects.create(unit_submission=unit_submission, name=exercise_name,
                                                   solution=solution)
                exercises.append(exercise)

        return exercises

    def register_self_evaluation(self, unit_submission):
        if self._has_submitted_self_evaluation():
            self_evaluation = SelfEvaluation.objects.create(unit_submission=unit_submission,
                                                            content_learning=self._self_evaluation['content_learning'],
                                                            exercises_autograde=self._self_evaluation[
                                                                'exercise_autograde'],
                                                            dedication_in_hours=self._self_evaluation[
                                                                'dedication_in_hours'],
                                                            dedication_evaluation=self._self_evaluation[
                                                                'dedication_evaluation'],
                                                            comment=self._self_evaluation['comment'])

            self._register_exercise_self_evaluations(self_evaluation, unit_submission)
        else:
            # TODO: hay que convertir a que la SelfEvaluation pueda tener multiples UnitSubmissions.
            pass

    def _register_exercise_self_evaluations(self, self_evaluation, unit_submission):
        for exercise_name, grade in self._self_evaluation['exercise_self_evaluation'].items():
            ExerciseSelfEvaluation.objects.create(self_evaluation=self_evaluation, exercise_name=exercise_name,
                                                  grade=grade)

    def _file_is_loaded(self, solution):
        return solution != 'undefined'

    def _has_submitted_self_evaluation(self):
        return self._self_evaluation != {}

    def _format_file_name_for_user(self, exercise_name, solution):
        old_name = solution.name
        solution.name = f'{datetime.now()}_{self.student_record().email[0:3]}_{old_name}'


class GetSelfEvaluationQuestionsCommand(Command):
    def __init__(self, user, unit):
        self._user = user
        self._unit = unit

    def validators(self):
        return [UserIsLoggedValidator(user=self._user)]

    def user(self):
        return self._user

    def unit(self):
        return self._unit

    def _execute_from_successful_validation(self, result):
        if not self._user_has_submitted_self_evaluation_for(self.unit()):
            result.set_object(self._self_evaluation_questions_and_responses())
        else:
            result.add_error(f'Autoevaluación ya realizada por {self.user()} para la unidad {self.unit()}')

        return result

    def _user_has_submitted_self_evaluation_for(self, unit):
        return SelfEvaluation.objects.filter(unit_submission__unit=unit,
                                             unit_submission__student_record__user=self.user()).exists()

    def _self_evaluation_questions_and_responses(self):
        self_evaluation_responses = SelfEvaluationResponses()
        return {
            'content_learning': {
                'question': "¿Cómo te fue con los CONTENIDOS de la clase?",
                'responses': self_evaluation_responses.content_learning_responses(),
                'is_exercise_evaluation': False
            },
            'exercise_autograde': {
                'question': "¿Cómo te fue en general con los EJERCICIOS?",
                'responses': self_evaluation_responses.exercises_autograde_responses(),
                'is_exercise_evaluation': False
            },
            'exercise_self_evaluation': {
                'question': "Sobre los ejercicios específicos de la clase:",
                'responses': self_evaluation_responses.exercises_grade_responses(),
                'is_exercise_evaluation': True
            },
            'dedication_in_hours': {
                'question': "¿Cuántas horas estimás que te llevó leer la clase y terminar los ejercicios?",
                'responses': 'Integer',
                'is_exercise_evaluation': False
            },
            'dedication_evaluation': {
                'question': "Respecto al tiempo que te tomó leer el material y hacer los ejercicios:",
                'responses': self_evaluation_responses.dedication_evaluation_responses(),
                'is_exercise_evaluation': False
            },
            'comment': {
                'question': "¿Tenés algún comentario sobre la clase o los ejercicios?",
                'responses': 'String',
                'is_exercise_evaluation': False
            },
        }


class GetPublishedCorrectionsByUser(Command):
    def __init__(self, user):
        self._user = user

    def validators(self):
        return []

    def user(self):
        return self._user

    def _execute_from_successful_validation(self, result):
        student_record = StudentRecord.objects.get(user=self._user)

        # FIXME: hay que hacer que solo agarre la ultima entrega por unidad
        last_unit_submissions = UnitSubmission.objects.filter(student_record=student_record)

        correction = Correction.objects.filter(exercise__unit_submission__in=last_unit_submissions, published=True)
        result.set_object(correction)
        return result


class GetExercisesByUser(Command):
    def __init__(self, user):
        self._user = user

    def validators(self):
        return []

    def user(self):
        return self._user

    def _execute_from_successful_validation(self, result):
        student_record = StudentRecord.objects.get(user=self._user)

        submitted_exercises = Exercise.objects.filter(unit_submission__student_record=student_record)

        result.set_object(submitted_exercises)

        return result


class GetPairReviewCorrections(Command):
    def __init__(self, user):
        self._user = user

    def validators(self):
        return []

    def user(self):
        return self._user

    def _execute_from_successful_validation(self, result):
        student_record = StudentRecord.objects.get(user=self._user)

        pair_review_corrections = self._pair_review_corrections(student_record)

        result.set_object(pair_review_corrections)

        return result

    def _pair_review_corrections(self, student_record):
        raise NotImplementedError('subclass responsibility')


class GetPairReviewCorrectionsToReview(GetPairReviewCorrections):
    def _pair_review_corrections(self, student_record):
        return PairReviewCorrection.objects.filter(reviewer=student_record)


class GetReviewedPairReviewCorrections(GetPairReviewCorrections):
    def _pair_review_corrections(self, student_record):
        return PairReviewCorrection.objects.filter(exercise__unit_submission__student_record=student_record, done=True,
                                                   published=True)


class SubmitPairReviewCorrection(Command):
    def __init__(self, user_id, exercise_id, comment, is_anonymous_reviewer):
        self._user_id = user_id
        self._exercise_id = exercise_id
        self._comment = comment
        self._is_anonymous_reviewer = is_anonymous_reviewer

    def validators(self):
        return [UserIsLoggedValidator(user=self._user_id)]

    def user(self):
        return self._user_id

    def exercise(self):
        return Exercise.objects.get(id=self._exercise_id)

    def comment(self):
        return self._comment

    def _execute_from_successful_validation(self, result):
        try:
            student_record = StudentRecord.objects.get(user=self.user())

            pair_review_correction = PairReviewCorrection.objects.get(exercise_id=self._exercise_id,
                                                                      reviewer=student_record,
                                                                      is_anonymous_reviewer=self._is_anonymous_reviewer)

            pair_review_correction.correct(comment=self.comment())
            pair_review_correction.save()
            result.set_object(pair_review_correction)
        except Exception:
            result.add_error(f'No se pudo realizar la Revision entre pares de {self.user()}')

        return result


class GetAuthomaticCorrections(Command):
    def __init__(self, user):
        self._user = user

    def validators(self):
        return []

    def user(self):
        return self._user

    def _execute_from_successful_validation(self, result):
        student_record = StudentRecord.objects.get(user=self._user)

        authomatic_corrections = AuthomaticCorrection.objects.filter(exercise__unit_submission__student_record=student_record,
                                                                     published=True)

        result.set_object(authomatic_corrections)

        return result


class GetStudents(Command):
    def __init__(self, user_id):
        self._user_id = user_id

    def validators(self):
        return [UserIsStaffValidator(user_id=self._user_id)]

    def user(self):
        return self._user_id

    def _execute_from_successful_validation(self, result):
        current_course = CourseRecord.current()
        students = StudentRecord.objects.filter(course=current_course, user__isnull=False)

        result.set_object(students)

        return result
