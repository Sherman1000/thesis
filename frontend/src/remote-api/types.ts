export type User = {
  id: string
  name: string
  is_teacher: boolean
}

export type SignUpUserData = {
  email: string
  is_registered: boolean
}

export type UserData = {
  user: User
  token: string
}

export type SelfEvaluationResponseOptions = {
  [key: string]: string
}

export type QuestionData = {
  is_exercise_evaluation: boolean
  question: string
  responses: any // todo fix
}

export type SelfEvaluationQuestions = {
  [key: string]: QuestionData
}

export type UnitCorrection = {
  unit: number
  exercise: string
  reviewer: string
  exercise_solution: string
  correction: string
  datetime: string
}

export type UnitsCorrections = UnitCorrection[]

export type CorrectionsByUnit = {
  [key: string]: {
    exercise: string
    reviewer: string
    exercise_solution: string
    correction: string
    datetime: string
  }[]
}

export type ApiResponse<T> = {
  success: boolean
  data?: T
  errors?: string
}

export type ExerciseSubmissions = ExerciseSubmission[]

export type ExerciseSubmission = {
  unit: number
  name: string
  solution: string
  datetime: string
}

type Exercise = {
  id: string
  unit: number
  name: string
  solution: string
  datetime: string
}

export type Review = {
  comment_for_author: string
  comment_from_author: string
  datetime: string
  done: boolean
  exercise: Exercise
}

export type Reviews = Review[]

export type AutomaticCorrection = {
  exercise: Exercise
  executed_instruction: string
  evaluated_code: string
  correct_tests_percentage: string
  recommendations: string[]
  errors: string[]
  datetime: string
  worked: boolean
}

export type AutomaticCorrections = AutomaticCorrection[]

export type Student = {
  email: string
  name: string
  surname: string
  user: User
}

export type Students = Student[]
