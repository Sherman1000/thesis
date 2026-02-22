export type Props = {
  loginUser: (email: string, password: string) => void;
  accessError?: boolean
}

export type State = {
  email?: string
  password?: string
}