export type Props = {
  onReviewsLoad: () => void
  selectedStudent?: string
}

export type State = {
  submissionStatus: {[key: string]: string}
  reviewsLoading: boolean
  reviewsFetchError: boolean
  reviews?: ReviewsByUnit
  message: string,
}

export type ReviewByUnit = {
  id: string
  unit: string
  authorMsg?: string
  reviewerMsg?: string
  reviewed: boolean
  exercise: string
  exerciseSolution: string
}

export type ReviewsByUnit = {
  [key: string]: ReviewByUnit[]
}
