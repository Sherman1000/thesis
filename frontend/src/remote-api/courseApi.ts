import { RequestHelper } from './requestHelper'
import { LocalStorage } from './localStorage'
import {
  AutomaticCorrections,
  ExerciseSubmissions,
  Reviews,
  SelfEvaluationQuestions,
  UnitsCorrections,
  Students,
} from './types'
import { Response } from './response'

export class CourseApi {
  private helper: RequestHelper

  constructor() {
    this.helper = new RequestHelper()
  }

  private static baseUrl() {
    return 'http://127.0.0.1/api/'
    return process.env.REACT_APP_BASE_URL
  }

  async unitSubmission(
    unit: number,
    exercises?: any,
    acceptsPairReview?: string,
    pairReviewComment?: string,
    selfEvaluation?: any
  ): Promise<Response<SelfEvaluationQuestions> | undefined> {
    const user = LocalStorage.fetchUser()
    const formData = new FormData()
    formData.append('user_id', user ? user.id : '')
    formData.append('unit', unit.toString())
    acceptsPairReview &&
      formData.append('accepts_pair_review', acceptsPairReview)
    pairReviewComment &&
      formData.append('pair_review_comment', pairReviewComment)
    selfEvaluation &&
      formData.append('self_evaluation', JSON.stringify(selfEvaluation))

    if (exercises) {
      const exerciseNames: string[] = []
      Object.keys(exercises).forEach((exerciseName: string) => {
        formData.append(exerciseName, exercises[exerciseName])
        exerciseNames.push(exerciseName)
      })
      formData.append('exercises', JSON.stringify(exerciseNames))
    }

    const url = `${CourseApi.baseUrl()}unit_submission`
    return this.helper.post(url, formData)
  }

  selfEvaluationQuestions(
    unit: number
  ): Promise<Response<SelfEvaluationQuestions> | undefined> {
    const user = LocalStorage.fetchUser()
    const userId = user ? user.id : ''
    const url = `${CourseApi.baseUrl()}self_evaluation_questions/${userId}/${unit}`
    return this.helper.get<SelfEvaluationQuestions>(url)
  }

  unitsCorrections(
    userId: string = ''
  ): Promise<Response<UnitsCorrections> | undefined> {
    const url = `${CourseApi.baseUrl()}corrections/${userId}`
    return this.helper.get<UnitsCorrections>(url)
  }

  exerciseSubmissions(
    userId: string = ''
  ): Promise<Response<ExerciseSubmissions> | undefined> {
    const url = `${CourseApi.baseUrl()}submissions/${userId}`
    return this.helper.get<ExerciseSubmissions>(url)
  }

  createCorrection(
    userId: string,
    exerciseId: string,
    message: string
  ): Promise<Response<null> | undefined> {
    const url = `${CourseApi.baseUrl()}submit_pair_reviews/${userId}`
    const body = {
      exercise_id: exerciseId,
      comment: message,
    }

    return this.helper.post<null>(url, body)
  }

  unitsPeerPendingCorrections(
    userId: string = ''
  ): Promise<Response<Reviews> | undefined> {
    const url = `${CourseApi.baseUrl()}to_pair_review/${userId}`
    return this.helper.get<Reviews>(url)
  }

  unitsPeerReviewedCorrections(
    userId: string = ''
  ): Promise<Response<Reviews> | undefined> {
    const url = `${CourseApi.baseUrl()}pair_reviews/${userId}`
    return this.helper.get<Reviews>(url)
  }

  automaticCorrections(
    userId: string = ''
  ): Promise<Response<AutomaticCorrections> | undefined> {
    const url = `${CourseApi.baseUrl()}authomatic_corrections/${userId}`
    return this.helper.get<AutomaticCorrections>(url)
  }

  students(): Promise<Response<Students> | undefined> {
    const user = LocalStorage.fetchUser()
    const userId = user ? user.id : ''
    const url = `${CourseApi.baseUrl()}students/${userId}`

    return this.helper.get<Students>(url)
  }
}
