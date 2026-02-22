export type Props = {
  onSubmissionsLoad: () => void
  selectedStudent?: string
}

export type State = {
  submissionsLoading: boolean
  submissionsFetchError: boolean
  submissions?: SubmissionsByUnit
}

export type SubmissionsByUnit = {
  [key: string]: {
    exerciseName: string
    exerciseSolution: string
    date: string
  }[]
}
