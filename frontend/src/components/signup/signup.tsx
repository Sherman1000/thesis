import * as React from 'react'
import { loginPath } from '../../routes'
import { Button, Form } from 'react-bootstrap'
import './signup.css'
import { Props, State } from './types'
import { UserApi } from '../../remote-api/userApi'

export default class Signup extends React.Component<Props, State> {
  PASSWORD_MIN_LENGTH = 8
  PASSWORD_MAX_LENGTH = 15

  private userApi: UserApi

  constructor(props: Props) {
    super(props)
    this.userApi = new UserApi()
    this.state = {
      email: { isInvalid: false },
      password: { isInvalid: false },
      confirmationPassword: { isInvalid: false },
      userDataLoading: false,
      existingUser: false,
    }

    this.fetchUserData = this.fetchUserData.bind(this)
    this.handlePasswordChange = this.handlePasswordChange.bind(this)
    this.handleConfirmationPasswordChange =
      this.handleConfirmationPasswordChange.bind(this)
    this.validateFields = this.validateFields.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  fetchUserData() {
    const { hash } = this.props
    if (!hash) {
      return
    }

    this.setState({ userDataLoading: true })
    this.userApi
      .signUpUserData(hash)
      .then((response) => {
        if (!!response && response.isSuccessful()) {
          const data = response.data()
          const email = data ? data.email : ''
          this.setState({
            userDataLoading: false,
            email: { value: email, isInvalid: false },
          })
        } else {
          this.setState({ userDataLoading: false, existingUser: true })
        }
      })
      .catch(() => {
        this.setState({ userDataLoading: false })
      })
  }

  componentDidMount() {
    this.fetchUserData()
  }

  handlePasswordChange(event: React.ChangeEvent<HTMLInputElement>) {
    const value = event.target.value
    const isInvalid =
      !value ||
      value.length < this.PASSWORD_MIN_LENGTH ||
      value.length > this.PASSWORD_MAX_LENGTH
    this.setState({ password: { value, isInvalid } })
  }

  handleConfirmationPasswordChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { password } = this.state
    const confirmationPassword = event.target.value
    const isInvalid =
      !confirmationPassword || password.value !== confirmationPassword
    this.setState({
      confirmationPassword: { value: event.target.value, isInvalid },
    })
  }

  validateFields() {
    const { email, password, confirmationPassword } = this.state
    return (
      !email.isInvalid && !password.isInvalid && !confirmationPassword.isInvalid
    )
  }

  handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    event.stopPropagation()

    if (this.validateFields()) {
      const { email, password, confirmationPassword } = this.state
      const { signUpUser, hash } = this.props
      // @ts-ignore
      signUpUser(hash, email.value, password.value, confirmationPassword.value)
    }
  }

  render() {
    const { email, password, confirmationPassword, existingUser } = this.state
    const { creationError } = this.props
    return (
      <div className="app-form">
        <h2 className="app-form-header">Bienvenidx!</h2>

        <Form onSubmit={this.handleSubmit}>
          <Form.Group
            className="mb-3 signup-email"
            controlId="formEmail"
            data-testid="email"
          >
            <Form.Label>Email</Form.Label>
            <Form.Control
              required
              type="email"
              placeholder="nombre@ejemplo.com"
              value={email.value || ''}
              isInvalid={email.isInvalid}
              readOnly
            />
            <Form.Text id="mailHelpBlock" muted>
              Ingresá el mismo email al que te llegó la invitación.
            </Form.Text>
            <Form.Control.Feedback type="invalid">
              Dirección de email inválida
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group
            className="mb-3 signup-password"
            controlId="formPassword"
            data-testid="password"
          >
            <Form.Label>Contraseña</Form.Label>
            <Form.Control
              required
              type="password"
              placeholder="Contraseña"
              value={password.value || ''}
              onChange={this.handlePasswordChange}
              isInvalid={password.isInvalid}
            />
            <Form.Text id="passwordHelpBlock" muted>
              Tu contraseña debe tener entre 8-15 caracteres.
            </Form.Text>
          </Form.Group>

          <Form.Group
            className="mb-3 signup-confirmation-password"
            controlId="formConfirmationPassword"
            data-testid="confirmation-password"
          >
            <Form.Label>Repetí contraseña</Form.Label>
            <Form.Control
              required
              type="password"
              placeholder="Repetí contraseña"
              value={confirmationPassword.value || ''}
              onChange={this.handleConfirmationPasswordChange}
              isInvalid={confirmationPassword.isInvalid}
            />
            <Form.Control.Feedback type="invalid">
              Las contraseñas no coinciden.
            </Form.Control.Feedback>
          </Form.Group>

          <Button
            variant="primary"
            type="submit"
            className="signup-submit"
            data-testid="submit"
          >
            Crear cuenta
          </Button>

          <p className="login-msg">
            Ya tenés una cuenta? <a href={loginPath}> Ingresá acá</a>
          </p>

          <div hidden={!creationError} className="app-submit-error-msg">
            <span>
              Ocurrió un error al intentar crear tu usuario. Por favor, volvé a
              intentarlo mas tarde.
            </span>
          </div>

          <div hidden={!existingUser} className="app-submit-error-msg">
            <span>
              El usuario con email ${email.value} ya existe. Si querés modificar
              tu contraseña completá los datos, sino{' '}
              <a href={loginPath}> ingresá acá</a>.
            </span>
          </div>
        </Form>
      </div>
    )
  }
}
