import json
import urllib

from rest_framework import status
from rest_framework.response import Response

from app.commands import commands
from app.endpoints.base import Endpoint, LoggedInRequiredMixin


class LoginEndpoint(Endpoint):
    def _post_command(self, post_data):
        username = post_data['username']
        password = post_data['password']

        chained_commands = [commands.GetUserFromUsernameAndPasswordCommand, commands.LoginCommand]
        return commands.ChainCommands(commands=chained_commands, initial_args=(username, password))


class LogoutEndpoint(Endpoint, LoggedInRequiredMixin):
    def _post_command(self, post_data):
        user_id = post_data['user_id']
        chain_commands = [commands.GetUserCommand, commands.LogoutCommand]
        return commands.ChainCommands(commands=chain_commands, initial_args=user_id)


class RegisterUserEndpoint(Endpoint):
    def post(self, request, *args, **kwargs):
        request_data = request.data
        request_data['email_hash'] = kwargs['email_hash']

        result = self._post_command(post_data=request_data).execute()
        presented_result = self._present_result(result)
        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _post_command(self, post_data):
        email = post_data['email']
        password = post_data['password']
        password_confirmation = post_data['password_confirmation']
        email_hash = post_data['email_hash']

        return commands.RegisterUserOrChangePasswordCommand(email, password, password_confirmation, email_hash)


class StudentRegistrationStatusEndpoint(Endpoint):
    def get(self, request, *args, **kwargs):
        request_data = request.GET.copy()
        request_data['email_hash'] = kwargs['email_hash']

        result = self._get_command(request_data=request_data).execute()
        presented_result = self._present_result(result)
        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        email_hash = request_data['email_hash']
        return commands.GetStudentegistrationStatusCommand(email_hash=email_hash)


class RegisterUnitSubmissionsEndpoint(Endpoint):
    def post(self, request, *args, **kwargs):
        request_data = request.data
        result = self._post_command(post_data=request_data).execute()
        presented_result = self._present_result(result)

        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _post_command(self, post_data):
        user_id = json.loads(post_data['user_id'])
        unit = json.loads(post_data['unit'])
        exercises = self.raw_exercises_from(post_data)
        accepts_pair_review = json.loads(post_data.get('accepts_pair_review', 'false'))
        pair_review_comment = post_data.get('pair_review_comment', '')
        self_evaluation = json.loads(post_data.get('self_evaluation', {}))

        return commands.RegisterUnitSubmissionCommand(user_id, unit, exercises, accepts_pair_review,
                                                      pair_review_comment, self_evaluation)

    def raw_exercises_from(self, post_data):
        exercises = []
        for exercise_name in json.loads(post_data.get('exercises', [])):
            exercises.append((exercise_name, post_data[exercise_name]))

        return exercises


class SelfEvaluationEndpoint(Endpoint):
    def get(self, request, *args, **kwargs):
        request_data = {'user_id': kwargs['id'], 'unit': kwargs['unit']}
        result = self._get_command(request_data=request_data).execute()
        presented_result = self._present_result(result)
        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        user_id = request_data['user_id']
        unit = request_data['unit']

        return commands.GetSelfEvaluationQuestionsCommand(user_id, unit)


class PublishedCorrectionsForStudentEndpoint(Endpoint):
    def get(self, request, *args, **kwargs):
        request_data = {'user_id': kwargs['id']}

        result = self._get_command(request_data=request_data).execute()
        presented_result = self._present_result(result)

        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        user_id = request_data['user_id']

        return commands.GetPublishedCorrectionsByUser(user_id)


class SubmittedExercisesForStudentEndpoint(Endpoint):
    def get(self, request, *args, **kwargs):
        request_data = {'user_id': kwargs['id']}

        result = self._get_command(request_data=request_data).execute()
        presented_result = self._present_result(result)

        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        user_id = request_data['user_id']

        return commands.GetExercisesByUser(user_id)


class ExerciseToPairReviewForStudentEndpoint(Endpoint):
    def get(self, request, *args, **kwargs):
        request_data = {'user_id': kwargs['id']}

        result = self._get_command(request_data=request_data).execute()
        presented_result = self._present_result(result)

        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        user_id = request_data['user_id']

        return commands.GetPairReviewCorrectionsToReview(user_id)


class PairReviewCorrectionsForUserEndpoint(Endpoint):
    def get(self, request, *args, **kwargs):
        request_data = {'user_id': kwargs['id']}

        result = self._get_command(request_data=request_data).execute()
        presented_result = self._present_result(result)

        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        user_id = request_data['user_id']

        return commands.GetReviewedPairReviewCorrections(user_id)


class SubmitPairReviewEndpoint(Endpoint):
    def post(self, request, *args, **kwargs):
        request_data = request.data
        request_data['user_id'] = kwargs['id']

        result = self._post_command(request_data=request_data).execute()
        presented_result = self._present_result(result)

        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _post_command(self, request_data):
        user_id = request_data['user_id']
        exercise_id = request_data['exercise_id']
        comment = request_data['comment']
        is_anonymous_reviewer = request_data.get('is_anonymous_reviewer', True)

        return commands.SubmitPairReviewCorrection(user_id, exercise_id, comment, is_anonymous_reviewer)


class AuthomaticCorrectionsForUserEndpoint(Endpoint):
    def get(self, request, *args, **kwargs):
        request_data = {'user_id': kwargs['id']}

        result = self._get_command(request_data=request_data).execute()
        presented_result = self._present_result(result)

        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        user_id = request_data['user_id']

        return commands.GetAuthomaticCorrections(user_id)


class StudentsEndpoint(Endpoint):
    def get(self, request, *args, **kwargs):
        request_data = {'user_id': kwargs['id']}

        result = self._get_command(request_data=request_data).execute()
        presented_result = self._present_result(result)

        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        user_id = request_data['user_id']

        return commands.GetStudents(user_id)