import * as React from 'react'
import { Props, RevisionsByUnit, ReviewsByUnit, State } from './types'
import { UnitsReader } from '../../units/unitsReader'
import { CourseApi } from '../../remote-api/courseApi'
import { Review, Reviews } from '../../remote-api/types'
import Spinner from '../spinner/spinner'
import BootstrapTable from 'react-bootstrap-table-next'
import { Form } from 'react-bootstrap'
import {
  logPeerCorrections,
  logPeerCorrectionsError,
} from '../../GAEventsHandler'

export default class PairsCorrections extends React.Component<Props, State> {
  private unitsReader: UnitsReader
  private courseApi: CourseApi

  constructor(props: Props) {
    super(props)
    this.unitsReader = new UnitsReader()
    this.courseApi = new CourseApi()
    this.state = {
      revisionsLoading: false,
      revisionsFetchError: false,
    }
    this.renderReviews = this.renderReviews.bind(this)
    this.updateStateWithReviews = this.updateStateWithReviews.bind(this)
  }

  orderReviewsByUnit(reviews: Reviews | undefined): ReviewsByUnit | undefined {
    if (!reviews || reviews.length === 0) return

    const orderedReviews: ReviewsByUnit = {}
    reviews.forEach((review: Review) => {
      const unit = review.exercise.unit.toString()
      const processedCorrections = orderedReviews[unit] || []
      processedCorrections.push({
        unit,
        msg: review.comment_from_author,
        reviewerMsg: review.comment_for_author,
        datetime: review.exercise.datetime,
        exercise: review.exercise.name,
        exerciseSolution: review.exercise.solution,
      })
      orderedReviews[unit] = processedCorrections
    })
    return orderedReviews
  }

  updateStateWithReviews(reviews?: ReviewsByUnit) {
    this.setState({
      revisions: reviews,
      revisionsLoading: false,
      revisionsFetchError: !reviews,
    })
  }

  fetchPeerCorrections(userId: string = '') {
    if (!userId) {
      return
    }
    this.setState({ revisionsLoading: true })
    this.courseApi
      .unitsPeerReviewedCorrections(userId)
      .then((response) => {
        if (!!response && response.isSuccessful()) {
          logPeerCorrections()
          const reviews = this.orderReviewsByUnit(response.data())
          reviews && this.props.onReviewsLoad()
          this.updateStateWithReviews(reviews)
        } else {
          logPeerCorrectionsError()
          this.updateStateWithReviews()
        }
      })
      .catch(() => {
        logPeerCorrectionsError()
        this.updateStateWithReviews()
      })
  }

  componentWillReceiveProps(nextProps: Props) {
    if (nextProps.selectedStudent !== this.props.selectedStudent) {
      this.fetchPeerCorrections(nextProps.selectedStudent)
    }
  }

  componentDidMount() {
    const { selectedStudent } = this.props
    this.fetchPeerCorrections(selectedStudent)
  }

  renderReviews(unit: string) {
    const { revisions } = this.state
    if (!revisions) return null

    const unitRevisions = revisions[parseInt(unit)]
    if (!unitRevisions) return null

    const columns = [
      {
        dataField: 'datetime',
        text: 'Fecha de revisión  ',
      },
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
    ]

    const expandRow = {
      renderer: (row: RevisionsByUnit) => (
        <Form>
          <Form.Group className="mb-3" controlId="formMessage">
            <Form.Label>Mensaje para quien revisó</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              placeholder={row.msg}
              readOnly
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formMessage">
            <Form.Label>Mensaje del revisxr</Form.Label>
            <Form.Control
              required
              as="textarea"
              rows={3}
              placeholder={row.reviewerMsg}
              readOnly
            />
          </Form.Group>
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
          data={unitRevisions}
          columns={columns}
          expandRow={expandRow}
        />
      </div>
    )
  }

  renderUnitsRevisions() {
    const { revisionsFetchError, revisions } = this.state
    if (revisionsFetchError) {
      return (
        <div className="app-submit-error-msg">
          Hubo un problema al cargar las revisiones. Por favor intentalo mas
          tarde.
        </div>
      )
    }
    if (!revisions) {
      return <div>No hay revisiones disponibles.</div>
    }
    const units = this.unitsReader.listUnits()
    return units.map(this.renderReviews)
  }

  render() {
    const { revisionsLoading } = this.state
    return revisionsLoading ? <Spinner /> : this.renderUnitsRevisions()
  }
}
