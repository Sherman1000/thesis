import json
from datetime import datetime

from django.contrib.auth import get_user_model

from app.models import Correction, UnitSubmission, Exercise, StudentRecord
from app.models.authomatic_corrections import AuthomaticCorrection
from app.models.pair_review_corrections import PairReviewCorrection
from app.presenters.base import Presenter


class DatetimePresenter(Presenter):
    @classmethod
    def can_handle(cls, obj):
        return isinstance(obj, datetime)

    def present(self):
        datetime_ = self._obj
        return datetime_.strftime("%d/%m/%Y - %H:%M")


class UserPresenter(Presenter):
    @classmethod
    def can_handle(cls, obj):
        UserModel = get_user_model()
        return isinstance(obj, UserModel)

    def present(self):
        user = self._obj
        data = {
            'id': user.id,
            'name': user.username,
            'is_teacher': user.is_staff
        }
        return Presenter.for_this(data).present()


class StudentRecordPresenter(Presenter):
    @classmethod
    def can_handle(cls, obj):
        return isinstance(obj, StudentRecord)

    def present(self):
        student_record = self._obj
        data = {
            'email': student_record.email,
            'name': student_record.name,
            'surname': student_record.surname,
            'user': student_record.user
        }
        return Presenter.for_this(data).present()


class UnitSubmissionPresenter(Presenter):
    @classmethod
    def can_handle(cls, obj):
        return isinstance(obj, UnitSubmission)

    def present(self):
        unit_submission = self._obj
        data = {
            'unit': unit_submission.unit,
            'student': unit_submission.student_record.name,
            'datetime': unit_submission.datetime,
            'accepts_pair_review': unit_submission.accepts_pair_review
        }
        return Presenter.for_this(data).present()


class ExercisePresenter(Presenter):
    @classmethod
    def can_handle(cls, obj):
        return isinstance(obj, Exercise)

    def present(self):
        exercise = self._obj
        data = {
            'id': exercise.id,
            'unit': exercise.unit_submission.unit,
            'name': exercise.name,
            'solution': exercise.solution_link(),
            'datetime': exercise.unit_submission.datetime,
        }
        return Presenter.for_this(data).present()


class CorrectionPresenter(Presenter):
    @classmethod
    def can_handle(cls, obj):
        return isinstance(obj, Correction)

    def present(self):
        correction = self._obj
        data = {
            'unit': correction.exercise_unit(),
            'exercise': correction.exercise_name(),
            'reviewer': correction.reviewer.email,
            'exercise_solution': correction.exercise_solution(),
            'correction': correction.comment_for_author,
            'done': correction.done,
            'datetime': correction.exercise.unit_submission.datetime
        }
        return Presenter.for_this(data).present()


class PairReviewPresenter(Presenter):
    @classmethod
    def can_handle(cls, obj):
        return isinstance(obj, PairReviewCorrection)

    def present(self):
        pair_review_correction = self._obj
        data = {
            'exercise': pair_review_correction.exercise,
            'comment_from_author': pair_review_correction.comment_from_author(),
            'comment_for_author': pair_review_correction.comment_for_author,
            'reviewer_name': pair_review_correction.anonymized_reviewers_email(),
            'done': pair_review_correction.done,
            'datetime': pair_review_correction.correction_datetime
        }
        return Presenter.for_this(data).present()


class AuthomaticCorrectionPresenter(Presenter):
    @classmethod
    def can_handle(cls, obj):
        return isinstance(obj, AuthomaticCorrection)

    def present(self):
        authomatic_correction = self._obj
        data = {
            'exercise': authomatic_correction.exercise,
            'executed_instruction': authomatic_correction.executed_instruction,
            'is_original': authomatic_correction.is_original,
            'evaluated_code': authomatic_correction.evaluated_code,
            'correct_tests_percentage': authomatic_correction.correct_tests_percentage,
            'recommendations': json.loads(authomatic_correction.recommendations),
            'errors': json.loads(authomatic_correction.errors),
            'worked': authomatic_correction.worked,
            'datetime': authomatic_correction.correction_datetime
        }
        return Presenter.for_this(data).present()
