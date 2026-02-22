import { CorrectionsByUnit } from '../../remote-api/types'

export type Props = {
  onCorrectionsLoad: () => void
  selectedStudent?: string
}

export type State = {
  correctionsLoading: boolean
  correctionsFetchError: boolean
  corrections?: CorrectionsByUnit
}
