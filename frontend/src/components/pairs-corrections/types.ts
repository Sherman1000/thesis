export type Props = {
  onReviewsLoad: () => void
  selectedStudent?: string
}

export type State = {
  revisionsLoading: boolean
  revisionsFetchError: boolean
  revisions?: ReviewsByUnit
}

export type RevisionsByUnit = {
  unit: string
  msg?: string
  reviewerMsg?: string
  datetime: string
  exercise: string
  exerciseSolution: string
}

export type ReviewsByUnit = {
  [key: string]: RevisionsByUnit[]
}
