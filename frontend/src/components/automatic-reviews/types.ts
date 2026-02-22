export type Props = {
  onCorrectionsLoad: () => void
  selectedStudent?: string
}

export type State = {
  submissionStatus: { [key: string]: string }
  correctionsLoading: boolean
  correctionsFetchError: boolean
  corrections?: CorrectionsByUnit
  message: string
}

export type CorrectionByUnit = {
  id: string
  unit: string
  datetime: string
  exercise: string
  exerciseSolution: string
  evaluatedCode: string
  successfulTestsPercentage: string
  recommendations: string[]
  executedInstruction: string
  errors: string[]
  worked: boolean
  rowId: string
}

export type CorrectionsByUnit = {
  [key: string]: CorrectionByUnit[]
}
