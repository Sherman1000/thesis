import * as React from 'react'
import Signup from '../signup/signup'
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
} from 'react-router-dom'
import {
  correctionsPath,
  loginPath,
  programHomePath,
  programPath,
  signupPath,
  unitSubmissionPath,
} from '../../routes'
import { LocalStorage } from '../../remote-api/localStorage'
import Login from '../login/login'
import Course from '../course/course'
import UnitSubmission from '../unit-submission/unitSubmission'
import { EmailHashMatch, ProgramMatch, Props, State, UnitMatch } from './types'
import { UserApi } from '../../remote-api/userApi'
import './app.css'
import CourseNavbar from '../course-navbar/courseNavbar'
import Corrections from '../corrections/corrections'
import {
  initialize,
  initializeUser,
  logLocation, logSignUp,
  logUserLogin,
  logUserLoginError, logUserLogOut, logUserLogOutError,
  logUserSignUpError
} from "../../GAEventsHandler"

export default class App extends React.Component<Props, State> {
  private userApi: UserApi

  constructor(props: Props) {
    super(props)

    initialize()

    this.signUpUser = this.signUpUser.bind(this)
    this.loginUser = this.loginUser.bind(this)
    this.navigateTo = this.navigateTo.bind(this)
    this.programComponent = this.programComponent.bind(this)
    this.signupComponent = this.signupComponent.bind(this)
    this.loginComponent = this.loginComponent.bind(this)
    this.unitSubmissionComponent = this.unitSubmissionComponent.bind(this)
    this.logoutUser = this.logoutUser.bind(this)
    this.correctionsComponent = this.correctionsComponent.bind(this)
    this.unitSubmissionComponent = this.unitSubmissionComponent.bind(this)

    this.state = {
      creationError: false,
      accessError: false,
      logoutError: false,
    }
    this.userApi = new UserApi()
  }

  componentDidMount() {
    if (LocalStorage.hasUserData()) {
      const user = LocalStorage.fetchUser()
      user && initializeUser()
    }
  }

  navigateTo(eventKey: string): JSX.Element {
    window.location.pathname = eventKey
    return <Redirect to={eventKey} push={true} />
  }

  signUpUser(
    hash: string,
    userName: string,
    password: string,
    confirmationPassword: string
  ) {
    this.userApi
      .signUpUser(hash, userName, password, confirmationPassword)
      .then((response) => {
        if (response && response.isSuccessful()) {
          initializeUser()
          logSignUp()
          this.setState({ creationError: false })
          this.navigateTo(programHomePath)
        } else {
          logUserSignUpError()
          this.setState({creationError: true})
        }
      })
      .catch((ignore) => {
        logUserSignUpError()
        this.setState({ creationError: true })
      })
  }

  loginUser(username: string, password: string) {
    return this.userApi
      .loginUser(username, password)
      .then((response) => {
        if (response && response.isSuccessful()) {
          logUserLogin()
          this.setState({ accessError: false })
          this.navigateTo(programHomePath)
        } else {
          logUserLoginError()
          this.setState({accessError: true})
        }
      })
      .catch((ignore) => {
        logUserLoginError()
        this.setState({ accessError: true })
      })
  }

  logoutUser() {
    return this.userApi
      .logoutUser()
      .then((response) => {
        if (response && response.isSuccessful()) {
          logUserLogOut()
          this.navigateTo(loginPath)
        }
      })
      .catch((ignore) => {
        logUserLogOutError()
      })
  }

  signupComponent({ match }: EmailHashMatch) {
    if (LocalStorage.hasUserData()) return this.navigateTo(programHomePath)
    logLocation()
    return (
      <Signup
        signUpUser={this.signUpUser}
        hash={match.params.emailHash}
        creationError={this.state.creationError}
      />
    )
  }

  loginComponent() {
    if (LocalStorage.hasUserData()) return this.navigateTo(programHomePath)
    logLocation()
    return (
      <Login loginUser={this.loginUser} accessError={this.state.accessError} />
    )
  }

  programComponent({ match }: ProgramMatch) {
    if (!LocalStorage.hasUserData()) return this.navigateTo(loginPath)
    logLocation()
    const path = match.params['0']
    return <Course contentPath={path} />
  }

  correctionsComponent() {
    if (!LocalStorage.hasUserData()) return this.navigateTo(loginPath)
    logLocation()
    return <Corrections />
  }

  unitSubmissionComponent({ match }: UnitMatch) {
    logLocation()
    const unit = match.params.unitNumber
    return <UnitSubmission unit={unit} />
  }

  render() {
    return (
      <Router>
        <CourseNavbar
          loggedUser={LocalStorage.hasUserData()}
          logoutUser={this.logoutUser}
        />

        <Switch>
          <Route path={signupPath} component={this.signupComponent} />
          <Route path={loginPath} component={this.loginComponent} />
          <Route path={programPath} component={this.programComponent} />
          <Route path={correctionsPath} component={this.correctionsComponent} />
          <Route
            path={unitSubmissionPath}
            component={this.unitSubmissionComponent}
          />
          <Redirect to={programHomePath} />
        </Switch>
      </Router>
    )
  }
}
