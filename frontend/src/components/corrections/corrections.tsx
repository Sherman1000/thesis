import * as React from 'react'
import './corrections.css'
import { Props, State } from './types'
import { Form, Tab, Tabs } from 'react-bootstrap'
import ExerciseSubmissions from '../exercise-submissions/exerciseSubmissions'
import TeacherCorrections from '../teacher-corrections/teacherCorrections'
import PendingReviews from '../pending-reviews/pendingReviews'
import PairsCorrections from '../pairs-corrections/pairsCorrections'
import AutomaticReviews from '../automatic-reviews/automaticReviews'
import { LocalStorage } from '../../remote-api/localStorage'
import { logStudents, logStudentsError } from '../../GAEventsHandler'
import { CourseApi } from '../../remote-api/courseApi'
import { Students } from '../../remote-api/types'
import Spinner from '../spinner/spinner'

export default class Corrections extends React.Component<Props, State> {
  private courseApi: CourseApi

  constructor(props: Props) {
    super(props)
    this.courseApi = new CourseApi()

    this.state = {
      submissionsLoaded: false,
      correctionsLoaded: false,
      pendingReviewsLoaded: false,
      peerReviewsLoaded: false,
      automaticReviewsLoaded: false,
      studentsLoading: false,
      studentsFetchError: false,
    }

    this.handleSubmissionsLoad = this.handleSubmissionsLoad.bind(this)
    this.handleCorrectionsLoad = this.handleCorrectionsLoad.bind(this)
    this.handlePendingReviewsLoad = this.handlePendingReviewsLoad.bind(this)
    this.handlePeerReviewsLoad = this.handlePeerReviewsLoad.bind(this)
    this.handleAutomaticReviewsLoad = this.handleAutomaticReviewsLoad.bind(this)
    this.updateStateWithStudents = this.updateStateWithStudents.bind(this)
  }

  handleSubmissionsLoad() {
    this.setState({ submissionsLoaded: true })
  }

  handleCorrectionsLoad() {
    this.setState({ correctionsLoaded: true })
  }

  handlePendingReviewsLoad() {
    this.setState({ pendingReviewsLoaded: true })
  }

  handlePeerReviewsLoad() {
    this.setState({ peerReviewsLoaded: true })
  }

  handleAutomaticReviewsLoad() {
    this.setState({ automaticReviewsLoaded: true })
  }

  updateStateWithStudents(students?: Students) {
    this.setState({
      students,
      studentsLoading: false,
      studentsFetchError: !students,
    })
  }

  componentDidMount() {
    const user = LocalStorage.fetchUser()
    if (LocalStorage.isTeacher()) {
      this.setState({ studentsLoading: true })
      this.courseApi
        .students()
        .then((response) => {
          if (!!response && response.isSuccessful()) {
            logStudents()
            this.updateStateWithStudents(response.data())
          } else {
            logStudentsError()
            this.updateStateWithStudents()
          }
        })
        .catch(() => {
          logStudentsError()
          this.updateStateWithStudents()
        })
    } else {
      this.setState({ selectedStudent: user ? user.id : undefined })
    }
  }

  renderTabs() {
    const {
      correctionsLoaded,
      peerReviewsLoaded,
      pendingReviewsLoaded,
      automaticReviewsLoaded,
      selectedStudent,
    } = this.state
    const teachersTabClass = !correctionsLoaded ? 'd-none' : ''
    const peersTabClass = !peerReviewsLoaded ? 'd-none' : ''
    const pendingTabClass = !pendingReviewsLoaded ? 'd-none' : ''
    const automaticTabClass = !automaticReviewsLoaded ? 'd-none' : ''
    return (
      <Tabs
        defaultActiveKey="submissions"
        id="uncontrolled-tab-example"
        className="mb-3 mt-4"
      >
        <Tab eventKey="submissions" title="Entregas">
          <ExerciseSubmissions
            onSubmissionsLoad={this.handleSubmissionsLoad}
            selectedStudent={selectedStudent}
          />
        </Tab>
        <Tab
          eventKey="teacherCorrections"
          title="Correcciones de docentes"
          tabClassName={teachersTabClass}
        >
          <TeacherCorrections
            onCorrectionsLoad={this.handleCorrectionsLoad}
            selectedStudent={selectedStudent}
          />
        </Tab>
        <Tab
          eventKey="peerCorrections"
          title="Revisiones de tus pares"
          tabClassName={peersTabClass}
        >
          <PairsCorrections
            onReviewsLoad={this.handlePeerReviewsLoad}
            selectedStudent={selectedStudent}
          />
        </Tab>
        <Tab
          eventKey="pendingCorrections"
          title="Tus revisiones pendientes"
          tabClassName={pendingTabClass}
        >
          <PendingReviews
            onReviewsLoad={this.handlePendingReviewsLoad}
            selectedStudent={selectedStudent}
          />
        </Tab>
        <Tab
          eventKey="automaticCorrections"
          title="Correcciones automáticas"
          tabClassName={automaticTabClass}
        >
          <AutomaticReviews
            onCorrectionsLoad={this.handleAutomaticReviewsLoad}
            selectedStudent={selectedStudent}
          />
        </Tab>
      </Tabs>
    )
  }

  handleUserChange = (event: any) => {
    this.setState({
      selectedStudent: event.target.selectedOptions[0].id,
    })
  }

  renderCorrections() {
    const { students } = this.state
    return (
      <div className="content">
        <h2>Detalle de entregas y correcciones</h2>

        {students && (
          <Form.Group className="mb-3" controlId="student">
            <Form.Label>Alumnx</Form.Label>
            <Form.Select onChange={this.handleUserChange}>
              <option value="" />
              {students.map((student) => (
                <option value={student.email} id={student.user.id}>
                  {student.email}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
        )}

        {this.renderTabs()}
      </div>
    )
  }

  render() {
    const { studentsLoading } = this.state
    return studentsLoading ? <Spinner /> : this.renderCorrections()
  }
}
