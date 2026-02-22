import {SelfEvaluationQuestions} from "../../remote-api/types"

export type Props = {
  unit: number
}

export type State = {
  questions?: SelfEvaluationQuestions
  questionsLoading: boolean
  selfEvaluationCompleted?: boolean
  acceptsPairReview?: string
  pairReviewComment?: string
  fileExercises?: {
    [key: string]: File
  }
  [key: string]: any
  submissionStatus: string
}