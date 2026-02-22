export type Props = {}

export type State = {
  creationError: boolean
  accessError: boolean
  logoutError: boolean
}

export type EmailHashMatch = {
  match: { params: { emailHash: string } }
}

export type ProgramMatch = {
  match: { params: { [key: string]: string } }
}

export type UnitMatch = {
  match: { params: { unitNumber: number } }
}
