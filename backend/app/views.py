import csv
import random

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from app.entities.importers import AuthomaticCorrectionImporter
from app.entities.students import StudentRegistrar
from app.forms import CsvImportForm, UnitToCorrectForm
from app.models import Exercise, Correction, UnitSubmission, CourseRecord
from app.models.courses.registries import PersistentCourseRegistry
from app.models.pair_review_corrections import PairReviewCorrection
from app.models.student.registries import PersistentStudentRegistry, PersistentStudiesRegistry, PersistentJobRegistry


class RegisterStudentView(View):
    # FIXME: This url is not protected by user. Anyone can enter
    def get(self, request):
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "student_record/csv_form.html", payload
        )

    def post(self, request):
        file = request.FILES['csv_file']
        decoded_file = file.read().decode('utf-8').splitlines()
        student_requests = csv.DictReader(decoded_file)

        course_registry = PersistentCourseRegistry()
        student_registry = PersistentStudentRegistry(course_registry=course_registry)
        studies_registry = PersistentStudiesRegistry()
        job_registry = PersistentJobRegistry()
        StudentRegistrar(student_registry, studies_registry=studies_registry, job_registry=job_registry,
                         course=course_registry.current()).process(student_requests)

        # FIXME: como haces el message user para dar feedback en el backend?
        # self.message_user(request, "Your csv file has been imported")
        return HttpResponseRedirect(reverse('admin:app_studentrecord_changelist'))


class CreateCorrectionsView(View):
    # FIXME: This url is not protected by user. Anyone can enter
    def get(self, request):
        form = UnitToCorrectForm()
        payload = {"form": form}
        return render(
            request, "corrections/unit_to_correct_form.html", payload
        )

    def post(self, request):
        unit = request.POST['unit']
        # TODO: THIS NEEDS REFACTOR. INCORRECT RESPONSIBILITIES
        exercises = Exercise.for_unit(unit)
        exercises = self._exercises_without_pending_correction(exercises)
        self._assign_exercises_to_reviewers(exercises)

        return HttpResponseRedirect(reverse('admin:app_correction_changelist'))

    def _assign_exercises_to_reviewers(self, exercises):
        for exercise in exercises:
            correction = Correction.for_exercise(exercise)
            correction.save()

    def _exercises_without_pending_correction(self, exercises):
        return [exercise for exercise in exercises if not hasattr(exercise, 'correction')]


class CreatePairReviewsView(View):
    # FIXME: This url is not protected by user. Anyone can enter
    def get(self, request):
        form = UnitToCorrectForm()
        payload = {"form": form}
        return render(
            request, "pair_review/unit_to_pair_review_form.html", payload
        )

    def post(self, request):
        unit = int(request.POST['unit'])
        # TODO: THIS NEEDS REFACTOR. INCORRECT RESPONSIBILITIES
        submissions_for_pair_review = self._submission_for_pair_review(unit)
        self._create_pair_review_corrections(submissions_for_pair_review, unit)

        return HttpResponseRedirect(reverse('admin:app_pairreviewcorrection_changelist'))

    def _submission_for_pair_review(self, unit):
        exercise_name = self._pair_review_exercise_name_for(unit)

        unit_submissions = UnitSubmission.objects.filter(accepts_pair_review=True, unit=unit,
                                                         exercises__name__contains=exercise_name).order_by('datetime')
        latest_submission_by_student = self._latest_submission_by_student(unit_submissions)

        return latest_submission_by_student.values()

    def _latest_submission_by_student(self, unit_submissions):
        latest_submissions = {}
        for unit_submission in unit_submissions:
            latest_submissions[unit_submission.student_record] = unit_submission

        return latest_submissions

    def _create_pair_review_corrections(self, unit_submissions, unit):
        exercise_name = self._pair_review_exercise_name_for(unit)

        paired_unit_submissions = self._assign_submissions_to_reviewers(unit_submissions)

        for unit_submission, reviewer in paired_unit_submissions:
            exercise = unit_submission.exercises.get(name=exercise_name)
            PairReviewCorrection.objects.create(exercise=exercise, reviewer=reviewer)

    def _assign_submissions_to_reviewers(self, unit_submissions):
        reviewers = [unit_submission.student_record for unit_submission in unit_submissions]
        shuffled_reviewers = random.sample(reviewers, len(reviewers))
        paired_unit_submissions = self._paired_unit_submissions(unit_submissions, shuffled_reviewers)

        return paired_unit_submissions

    def _paired_unit_submissions(self, unit_submissions, reviewers):
        assigned_submissions = []
        for unit_submission in unit_submissions:
            random_submission = self._random_reviewer(unit_submission, reviewers,
                                                      already_assigned_submissions=assigned_submissions)

            assigned_submissions.append((unit_submission, random_submission))

        return assigned_submissions

    def _random_reviewer(self, unit_submission, reviewers, already_assigned_submissions, max_assigments=2):
        for reviewer in reviewers:
            if not self._is_reviewer_submission(reviewer, unit_submission) and \
                    not self._is_already_assigned(reviewer, already_assigned_submissions) and \
                    self._has_less_than(max_assigments, of_unit_submission=unit_submission,
                                        in_already_assigned_submissions=already_assigned_submissions,
                                        reviewer=reviewer) and \
                    not self._has_already_reviewed_that_student(reviewer, unit_submission):
                return reviewer
        raise Exception('Fail to pair the corrections')

    def _is_reviewer_submission(self, reviewer, unit_submission):
        return reviewer == unit_submission.student_record

    def _has_less_than(self, max_assigments, of_unit_submission, in_already_assigned_submissions, reviewer):
        already_assigned_submissions = in_already_assigned_submissions
        unit_submission = of_unit_submission

        reviewer_corrections = PairReviewCorrection.objects.filter(exercise__unit_submission__unit=unit_submission.unit,
                                                                   reviewer=reviewer)
        reviewer_corrections_amount = reviewer_corrections.count()

        # assigned_unit_submission = [assigment[0] == unit_submission for assigment in already_assigned_submissions]
        # assigned_unit_submission_amount = len(assigned_unit_submission)
        return reviewer_corrections_amount < max_assigments

    def _has_already_reviewed_that_student(self, reviewer, unit_submission):
        return PairReviewCorrection.objects.filter(exercise__unit_submission__unit=unit_submission.unit,
                                                   exercise__unit_submission__student_record__email=unit_submission.student_record.email,
                                                   reviewer=reviewer).exists()

    def _is_already_assigned(self, reviewer, already_assigned_submissions):
        return any([self.assigned_reviewer(assigment) == reviewer for assigment in already_assigned_submissions])

    def assigned_reviewer(self, assigment):
        return assigment[1]

    def _pair_review_exercise_name_for(self, unit):
        return {
            1: 'geringoso.py',
            2: 'informe.py',
            3: 'tabla_informe.py',
            4: 'propaga.py',
            5: 'figuritas.py',
            6: 'costo_camion.py',
            7: 'random_walk.py',
            8: 'arbolado_parques_veredas.py',
            9: 'torre_control.py'
        }[unit]


class ExportForAuthomaticCorrectionsView(View):
    # FIXME: This url is not protected by user. Anyone can enter
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export_exercises.csv'
        current_course = CourseRecord.objects.last()
        items = Exercise.objects.filter(unit_submission__student_record__course=current_course)

        self._write_csv(response, items=items)

        return response

    def _write_csv(self, response, items):
        writer = csv.writer(response)
        self._write_column_titles(writer)
        self._write_exercise_rows(writer, exercises=items)

    def _write_exercise_rows(self, writer, exercises):
        for exercise in exercises:
            row = [exercise.id, exercise.student_record().id, exercise.student_record().email,
                   exercise.unit(), exercise.name, exercise.delivery_date(), exercise.version(),
                   exercise.download_link()]
            writer.writerow(row)

    def _write_column_titles(self, writer):
        column_names = ['id_archivo', 'id_persona', 'email', 'unidad', 'ejercicio', 'fecha_entrega', 'version',
                        'solucion']
        writer.writerow(column_names)


class RegisterAuthomaticCorrectionView(View):
    # FIXME: This url is not protected by user. Anyone can enter
    def get(self, request):
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "authomatic_corrections/csv_form.html", payload
        )

    def post(self, request):
        file = request.FILES['csv_file']
        decoded_file = file.read().decode('utf-8').splitlines()
        authomatic_corrections = csv.DictReader(decoded_file)

        AuthomaticCorrectionImporter().import_corrections(authomatic_corrections)

        # FIXME: como haces el message user para dar feedback en el backend?
        # self.message_user(request, "Your csv file has been imported")
        return HttpResponseRedirect(reverse('admin:app_authomaticcorrection_changelist'))
