"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from app.endpoints import endpoints
from app.views import RegisterStudentView, CreateCorrectionsView, CreatePairReviewsView, \
    ExportForAuthomaticCorrectionsView, RegisterAuthomaticCorrectionView

urlpatterns = [
    path(r'admin/import-students/', RegisterStudentView.as_view(), name='register_student_view'),
    path(r'admin/import-authomatic-corrections/', RegisterAuthomaticCorrectionView.as_view(), name='register_authomatic_correction_view'),
    path(r'admin/create-corrections', CreateCorrectionsView.as_view(), name='create_corrections_view'),
    path(r'admin/create-pair_reviews', CreatePairReviewsView.as_view(), name='create_pair_reviews_view'),
    path(r'admin/export-authomatic-corrections', ExportForAuthomaticCorrectionsView.as_view(), name='export_for_authomatic_corrections_view'),
    # Importa el orden acá. Fijarse de mover las de arriba a get_urls de cada modelo del admin.
    path('admin/', admin.site.urls),

    path('api/register/<str:email_hash>', endpoints.RegisterUserEndpoint.as_view(), name='register_user_endpoint'),
    path('api/registration_status/<str:email_hash>', endpoints.StudentRegistrationStatusEndpoint.as_view(), name='student_registration_status_endpoint'),
    path('api/login', endpoints.LoginEndpoint.as_view(), name='login'),
    path('api/logout', endpoints.LogoutEndpoint.as_view(), name='logout'),
    path('api/unit_submission', endpoints.RegisterUnitSubmissionsEndpoint.as_view(), name='unit_submission'),
    path('api/students/<str:id>', endpoints.StudentsEndpoint.as_view(), name='students'),
    path('api/self_evaluation_questions/<str:id>/<str:unit>', endpoints.SelfEvaluationEndpoint.as_view(), name='self_evaluation_questions'),
    path('api/corrections/<str:id>', endpoints.PublishedCorrectionsForStudentEndpoint.as_view(), name='corrections_for_student'),
    path('api/to_pair_review/<str:id>', endpoints.ExerciseToPairReviewForStudentEndpoint.as_view(), name='exercises_to_pair_review'),
    path('api/pair_reviews/<str:id>', endpoints.PairReviewCorrectionsForUserEndpoint.as_view(), name='pair_reviews'),
    path('api/submit_pair_reviews/<str:id>', endpoints.SubmitPairReviewEndpoint.as_view(), name='submit_pair_reviews'),
    path('api/submissions/<str:id>', endpoints.SubmittedExercisesForStudentEndpoint.as_view(), name='submissions_for_student'),
    path('api/authomatic_corrections/<str:id>', endpoints.AuthomaticCorrectionsForUserEndpoint.as_view(), name='authomatic_corrections'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
