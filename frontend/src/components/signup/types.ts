export type Props = {
  signUpUser: (
    hash: string,
    email: string,
    password: string,
    confirmationPassword: string
  ) => void
  hash: string
  creationError?: boolean
}

type FieldValidation = {
  isInvalid: boolean
  value?: string
}

export type State = {
  email: FieldValidation
  password: FieldValidation
  confirmationPassword: FieldValidation
  userDataLoading: boolean
  existingUser: boolean
}
