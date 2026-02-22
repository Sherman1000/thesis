import * as React from 'react'
import { Props, ReviewByUnit, ReviewsByUnit, State } from './types'
import { UnitsReader } from '../../units/unitsReader'
import { CourseApi } from '../../remote-api/courseApi'
import { Review, Reviews } from '../../remote-api/types'
import Spinner from '../spinner/spinner'
import BootstrapTable from 'react-bootstrap-table-next'
import { Button, Form } from 'react-bootstrap'
import {
  logPeerReviewSubmission,
  logPeerReviewSubmissionError,
  logPendingPeerReview,
  logPendingPeerReviewError,
} from '../../GAEventsHandler'

export default class PendingReviews extends React.Component<Props, State> {
  private unitsReader: UnitsReader
  private courseApi: CourseApi

  SUCCESS_STATUS = 'success'
  ERROR_STATUS = 'error'

  constructor(props: Props) {
    super(props)
    this.unitsReader = new UnitsReader()
    this.courseApi = new CourseApi()
    this.state = {
      submissionStatus: {},
      reviewsLoading: false,
      reviewsFetchError: false,
      message: '',
    }
    this.renderReviews = this.renderReviews.bind(this)
    this.updateStateWithReviews = this.updateStateWithReviews.bind(this)
    this.handleMessageChange = this.handleMessageChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  orderReviewsByUnit(reviews: Reviews | undefined): ReviewsByUnit | undefined {
    if (!reviews || reviews.length === 0) return

    const orderedReviews: ReviewsByUnit = {}
    reviews.forEach((review: Review) => {
      const unit = review.exercise.unit.toString()
      const processedCorrections = orderedReviews[unit] || []
      processedCorrections.push({
        unit,
        authorMsg: review.comment_from_author,
        reviewerMsg: review.comment_for_author,
        reviewed: review.done,
        exercise: review.exercise.name,
        exerciseSolution: review.exercise.solution,
        id: review.exercise.id,
      })
      orderedReviews[unit] = processedCorrections
    })
    return orderedReviews
  }

  updateStateWithReviews(reviews?: ReviewsByUnit) {
    this.setState({
      reviews,
      reviewsLoading: false,
      reviewsFetchError: !reviews,
    })
  }

  fetchPeerPendingCorrections(userId: string = '') {
    if (!userId) {
      return
    }
    this.courseApi
      .unitsPeerPendingCorrections(userId)
      .then((response) => {
        if (!!response && response.isSuccessful()) {
          logPendingPeerReview()
          const reviews = this.orderReviewsByUnit(response.data())
          reviews && this.props.onReviewsLoad()
          this.updateStateWithReviews(reviews)
        } else {
          logPendingPeerReviewError()
          this.updateStateWithReviews()
        }
      })
      .catch(() => {
        logPendingPeerReviewError()
        this.updateStateWithReviews()
      })
  }

  componentWillReceiveProps(nextProps: Props) {
    if (nextProps.selectedStudent !== this.props.selectedStudent) {
      this.fetchPeerPendingCorrections(nextProps.selectedStudent)
    }
  }

  componentDidMount() {
    const { selectedStudent } = this.props
    this.fetchPeerPendingCorrections(selectedStudent)
  }

  handleMessageChange(event: React.ChangeEvent<HTMLInputElement>) {
    const value = event.target.value
    this.setState({ message: value })
  }

  handleSubmit(exerciseId: string) {
    const { selectedStudent } = this.props
    return (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault()
      event.stopPropagation()

      const updateSubmissionStatus = (
        submissionStatus: { [key: string]: string },
        newStatus: string
      ) => {
        const status = { ...submissionStatus }
        status[exerciseId] = newStatus
        this.setState({ submissionStatus: status })
      }

      const { message, submissionStatus } = this.state
      !!message &&
        this.courseApi
          .createCorrection(selectedStudent || '', exerciseId, message)
          .then((response) => {
            if (response && response.isSuccessful()) {
              logPeerReviewSubmission()
              updateSubmissionStatus(submissionStatus, this.SUCCESS_STATUS)
            } else {
              logPeerReviewSubmissionError()
              updateSubmissionStatus(submissionStatus, this.ERROR_STATUS)
            }
          })
          .catch((ignore) => {
            logPeerReviewSubmissionError()
            updateSubmissionStatus(submissionStatus, this.ERROR_STATUS)
          })
    }
  }

  renderSubmissionMsg(exerciseId: string) {
    const { submissionStatus } = this.state
    const exerciseStatus = submissionStatus[exerciseId]
    if (exerciseStatus === this.ERROR_STATUS) {
      return (
        <div className="app-submit-error-msg">
          <span>
            Ocurrió un error al enviar tus respuestas. Por favor, volvé a
            intentarlo mas tarde.
          </span>
        </div>
      )
    }
    if (exerciseStatus === this.SUCCESS_STATUS) {
      return (
        <div className="app-submit-success-msg">
          <span>Tus respuestas fueron enviadas con éxito!</span>
        </div>
      )
    }
  }

  renderReviews(unit: string) {
    const { reviews } = this.state
    if (!reviews) return null

    const unitReviews = reviews[parseInt(unit)]
    if (!unitReviews) return null

    const columns = [
      {
        dataField: 'exercise',
        text: 'Ejercicio',
      },
      {
        dataField: 'exerciseSolution',
        text: 'Archivo entregado',
        formatter: (editorProps: any, value: any) => (
          <div dangerouslySetInnerHTML={{ __html: value.exerciseSolution }} />
        ),
      },
      {
        dataField: 'reviewed',
        text: '¿Fue revisado?',
        formatter: (editorProps: any, value: any) => (
          <div>{value.reviewed ? 'Si' : 'No'}</div>
        ),
      },
    ]

    const expandRow = {
      renderer: (row: ReviewByUnit) => (
        <Form onSubmit={this.handleSubmit(row.id)}>
          <Form.Group className="mb-3" controlId="formMessage">
            <Form.Label>Mensaje del autxr</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              placeholder={row.authorMsg}
              readOnly
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formMessage">
            <Form.Label>Tu mensaje para el autxr</Form.Label>
            <Form.Control
              required
              as="textarea"
              rows={3}
              placeholder={row.reviewed ? row.reviewerMsg : 'Revisión...'}
              onChange={this.handleMessageChange}
              readOnly={row.reviewed}
            />
          </Form.Group>

          <Button variant="primary" type="submit" hidden={row.reviewed}>
            Enviar revisión
          </Button>

          {this.renderSubmissionMsg(row.id)}
        </Form>
      ),
      showExpandColumn: true,
      onlyOneExpanding: true,
    }

    return (
      <div className="unit-corrections-table">
        <h2>Unidad {unit}</h2>
        <BootstrapTable
          keyField="exercise"
          data={unitReviews}
          columns={columns}
          expandRow={expandRow}
        />
      </div>
    )
  }

  renderUnitsReviews() {
    const { reviewsFetchError, reviews } = this.state
    if (reviewsFetchError) {
      return (
        <div className="app-submit-error-msg">
          Hubo un problema al cargar tus correcciones pendientes. Por favor
          intentalo mas tarde.
        </div>
      )
    }
    if (!reviews) {
      return <div>No hay correcciones disponibles.</div>
    }
    const units = this.unitsReader.listUnits()
    return units.map(this.renderReviews)
  }

  render() {
    const { reviewsLoading } = this.state
    return reviewsLoading ? <Spinner /> : this.renderUnitsReviews()
  }
}
