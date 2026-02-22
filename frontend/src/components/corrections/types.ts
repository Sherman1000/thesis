import { Students } from '../../remote-api/types'

export type Props = {}

export type State = {
  submissionsLoaded: boolean
  correctionsLoaded: boolean
  pendingReviewsLoaded: boolean
  peerReviewsLoaded: boolean
  automaticReviewsLoaded: boolean
  studentsLoading: boolean
  studentsFetchError: boolean
  students?: Students
  selectedStudent?: string
}
