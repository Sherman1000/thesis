import * as React from "react";
import {Button, Form} from "react-bootstrap"
import {Props, State} from "./types"

export default class Login extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {}

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
  }

  handleEmailChange(event: React.ChangeEvent<HTMLInputElement>) {
    const value = event.target.value;
    this.setState({email: value});
  }

  handlePasswordChange(event: React.ChangeEvent<HTMLInputElement>) {
    const value = event.target.value;
    this.setState({password: value});
  }

  handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    event.stopPropagation();

    const {email, password} = this.state
    email && password && this.props.loginUser(email, password);
  };

  render() {
    const {accessError} = this.props
    return (
      <div className="app-form">
        <h2 className="app-form-header">Bienvenidx!</h2>

        <Form onSubmit={this.handleSubmit}>
          <Form.Group className="mb-3" controlId="formEmail">
            <Form.Label>Email</Form.Label>
            <Form.Control required type="email" placeholder="nombre@ejemplo.com" onChange={this.handleEmailChange}/>
            <Form.Control.Feedback type="invalid">Dirección de email inválida</Form.Control.Feedback>
          </Form.Group>

          <Form.Group className="mb-3" controlId="formPassword">
            <Form.Label>Contraseña</Form.Label>
            <Form.Control required type="password" placeholder="Contraseña" onChange={this.handlePasswordChange}/>
          </Form.Group>

          <Button variant="primary" type="submit">
            Ingresar
          </Button>

          <div hidden={!accessError} className="app-submit-error-msg">
            <span>Ocurrió un error al intentar acceder. Por favor, volvé a intentarlo mas tarde.</span>
          </div>

        </Form>
      </div>
    )
  }
}
