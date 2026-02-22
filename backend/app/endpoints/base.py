from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.commands.commands import ByPassCommand
from app.presenters.base import Presenter


class LoggedInRequiredMixin:
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class Endpoint(APIView):
    """
    Todo: only GET and POST are defined. PUT, PATCH, etc are not implemented, do it if you need to
    """

    def get(self, request, *args, **kwargs):
        result = self._get_command(request_data=request.GET).execute()
        presented_result = self._present_result(result)
        return Response(data=presented_result, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        result = self._post_command(post_data=request.data).execute()
        presented_result = self._present_result(result)
        return Response(data=presented_result, status=status.HTTP_200_OK)

    def _get_command(self, request_data):
        # override this method if the endpoint is a GET request
        return ByPassCommand()

    def _post_command(self, post_data):
        # override this method if the endpoint is a POST request
        return ByPassCommand()

    def _present_result(self, result):
        return {
            'success': result.is_successful(),
            'data': self._get_data_from_result(result),
            'errors': result.errors(),
        }

    def _get_data_from_result(self, result):
        data = result.get_object()
        presented_data = self._get_presenter().for_this(data).present()
        return presented_data

    def _get_presenter(self):
        return Presenter
