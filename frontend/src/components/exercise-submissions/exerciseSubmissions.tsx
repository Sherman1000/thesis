import * as React from 'react'
import { Props, State, SubmissionsByUnit } from './types'
import { UnitsReader } from '../../units/unitsReader'
import { CourseApi } from '../../remote-api/courseApi'
import {
  ExerciseSubmissions as Submissions,
  ExerciseSubmission as Submission,
} from '../../remote-api/types'
import Spinner from '../spinner/spinner'
import BootstrapTable from 'react-bootstrap-table-next'
import {
  logExerciseSubmission,
  logExerciseSubmissionError,
} from '../../GAEventsHandler'

export default class ExerciseSubmissions extends React.Component<Props, State> {
  private unitsReader: UnitsReader
  private courseApi: CourseApi

  constructor(props: Props) {
    super(props)
    this.unitsReader = new UnitsReader()
    this.courseApi = new CourseApi()
    this.state = { submissionsLoading: false, submissionsFetchError: false }

    this.renderUnitSubmissions = this.renderUnitSubmissions.bind(this)
  }

  orderSubmissionsByUnit(
    submissions: Submissions | undefined
  ): SubmissionsByUnit | undefined {
    if (!submissions) return

    const orderedSubmissions: SubmissionsByUnit = {}
    submissions.forEach((submission: Submission) => {
      const unit = submission.unit.toString()
      const processedSubmissions = orderedSubmissions[unit] || []
      processedSubmissions.push({
        exerciseName: submission.name,
        exerciseSolution: submission.solution,
        date: submission.datetime,
      })
      orderedSubmissions[unit] = processedSubmissions
    })
    return orderedSubmissions
  }

  updateStateWithSubmissions(submissions?: SubmissionsByUnit) {
    this.setState({
      submissions: submissions,
      submissionsLoading: false,
      submissionsFetchError: !submissions,
    })
  }

  fetchExerciseSubmissions(userId: string = '') {
    if (!userId) {
      return
    }
    this.setState({ submissionsLoading: true })
    this.courseApi
      .exerciseSubmissions(userId)
      .then((response) => {
        this.props.onSubmissionsLoad()
        if (!!response && response.isSuccessful()) {
          logExerciseSubmission()
          const submissions = this.orderSubmissionsByUnit(response.data())
          this.updateStateWithSubmissions(submissions)
        } else {
          logExerciseSubmissionError()
          this.updateStateWithSubmissions()
        }
      })
      .catch(() => {
        logExerciseSubmissionError()
        this.props.onSubmissionsLoad()
        this.updateStateWithSubmissions()
      })
  }

  componentWillReceiveProps(nextProps: Props) {
    if (nextProps.selectedStudent !== this.props.selectedStudent) {
      this.fetchExerciseSubmissions(nextProps.selectedStudent)
    }
  }

  componentDidMount() {
    const { selectedStudent } = this.props
    this.fetchExerciseSubmissions(selectedStudent)
  }

  renderUnitSubmissions(unit: string) {
    const { submissions } = this.state
    if (!submissions) return null

    const unitSubmissions = submissions[parseInt(unit)]
    if (!unitSubmissions) return null

    const columns = [
      {
        dataField: 'date',
        text: 'Fecha de entrega',
      },
      {
        dataField: 'exerciseName',
        text: 'Ejercicio',
      },
      {
        dataField: 'exerciseSolution',
        text: 'Archivo entregado',
        formatter: (editorProps: any, value: any) => (
          <div dangerouslySetInnerHTML={{ __html: value.exerciseSolution }} />
        ),
      },
    ]

    return (
      <div className="unit-submissions-table">
        <h2>Unidad {unit}</h2>
        <BootstrapTable
          keyField="exerciseName"
          data={unitSubmissions}
          columns={columns}
        />
      </div>
    )
  }

  renderUnitsSubmissions() {
    const { submissionsFetchError, submissions } = this.state
    if (submissionsFetchError) {
      return (
        <div className="app-submit-error-msg">
          Hubo un problema al cargar tus entregas. Por favor intentalo mas
          tarde.
        </div>
      )
    }
    if (!submissions) {
      return <div>Todavía no entregaste ejercicios.</div>
    }
    const units = this.unitsReader.listUnits()
    return units.map(this.renderUnitSubmissions)
  }

  render() {
    const { submissionsLoading } = this.state
    return submissionsLoading ? <Spinner /> : this.renderUnitsSubmissions()
  }
}
