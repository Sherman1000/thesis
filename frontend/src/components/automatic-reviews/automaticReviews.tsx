import * as React from 'react'
import { Props, CorrectionByUnit, CorrectionsByUnit, State } from './types'
import { UnitsReader } from '../../units/unitsReader'
import { CourseApi } from '../../remote-api/courseApi'
import {
  AutomaticCorrection,
  AutomaticCorrections,
} from '../../remote-api/types'
import Spinner from '../spinner/spinner'
import BootstrapTable from 'react-bootstrap-table-next'
import {
  logAutomaticCorrections,
  logAutomaticCorrectionsError,
} from '../../GAEventsHandler'
import './automaticReviews.css'

export default class AutomaticReviews extends React.Component<Props, State> {
  private unitsReader: UnitsReader
  private courseApi: CourseApi

  constructor(props: Props) {
    super(props)
    this.unitsReader = new UnitsReader()
    this.courseApi = new CourseApi()
    this.state = {
      submissionStatus: {},
      correctionsLoading: false,
      correctionsFetchError: false,
      message: '',
    }
    this.renderCorrections = this.renderCorrections.bind(this)
    this.updateStateWithCorrections = this.updateStateWithCorrections.bind(this)
  }

  orderCorrectionsByUnit(
    corrections: AutomaticCorrections | undefined
  ): CorrectionsByUnit | undefined {
    if (!corrections || corrections.length === 0) return

    const orderedCorrections: CorrectionsByUnit = {}
    corrections.forEach((correction: AutomaticCorrection) => {
      const unit = correction.exercise.unit.toString()
      const processedCorrections = orderedCorrections[unit] || []
      processedCorrections.push({
        unit,
        id: correction.exercise.id,
        datetime: correction.exercise.datetime,
        exercise: correction.exercise.name,
        exerciseSolution: correction.exercise.solution,
        evaluatedCode: correction.evaluated_code,
        successfulTestsPercentage: correction.correct_tests_percentage,
        recommendations: correction.recommendations,
        executedInstruction: correction.executed_instruction,
        errors: correction.errors,
        worked: correction.worked,
        rowId: correction.exercise.id + '/' + correction.exercise.datetime,
      })
      orderedCorrections[unit] = processedCorrections
    })
    return orderedCorrections
  }

  updateStateWithCorrections(reviews?: CorrectionsByUnit) {
    this.setState({
      corrections: reviews,
      correctionsLoading: false,
      correctionsFetchError: !reviews,
    })
  }

  fetchAutomaticCorrections(userId: string = '') {
    if (!userId) {
      return
    }
    this.setState({ correctionsLoading: true })
    this.courseApi
      .automaticCorrections(userId)
      .then((response) => {
        if (!!response && response.isSuccessful()) {
          logAutomaticCorrections()
          const corrections = this.orderCorrectionsByUnit(response.data())
          corrections && this.props.onCorrectionsLoad()
          this.updateStateWithCorrections(corrections)
        } else {
          logAutomaticCorrectionsError()
          this.updateStateWithCorrections()
        }
      })
      .catch(() => {
        logAutomaticCorrectionsError()
        this.updateStateWithCorrections()
      })
  }

  componentWillReceiveProps(nextProps: Props) {
    if (nextProps.selectedStudent !== this.props.selectedStudent) {
      this.fetchAutomaticCorrections(nextProps.selectedStudent)
    }
  }

  componentDidMount() {
    const { selectedStudent } = this.props
    this.fetchAutomaticCorrections(selectedStudent)
  }

  renderCorrections(unit: string) {
    const { corrections } = this.state
    if (!corrections) return null

    const unitCorrections = corrections[parseInt(unit)]
    if (!unitCorrections) return null

    const columns = [
      {
        dataField: 'datetime',
        text: 'Fecha de entrega',
      },
      {
        dataField: 'exercise',
        text: 'Archivo corregido',
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
      renderer: (row: CorrectionByUnit) => (
        <div>
          <div>
            <div
              dangerouslySetInnerHTML={{ __html: row.executedInstruction }}
            />
            <hr />
          </div>

          <div hidden={!row.worked}>
            <div>
              El código que evaluamos fue:
              <div
                className="evaluated-code"
                dangerouslySetInnerHTML={{ __html: row.evaluatedCode }}
              />
              <hr />
            </div>

            <div>
              Y obtuvimos el siguiente resultado:{' '}
              {row.successfulTestsPercentage}% de tests correctos
              <ul hidden={row.recommendations.length === 0}>
                {row.recommendations.map((recommendation) => (
                  <li>{recommendation}</li>
                ))}
              </ul>
              <hr hidden={row.errors.length === 0} />
            </div>

            <div hidden={row.errors.length === 0}>
              Y al correr los test python arrojó:
              <ul>
                {row.errors.map((error) => (
                  <li>{error}</li>
                ))}
              </ul>
            </div>
          </div>

          <div hidden={row.worked}>
            <div>
              No pudimos correr la función. Detectamos el siguiente problema al
              correrlo:
              <ul hidden={row.recommendations.length === 0}>
                {row.recommendations.map((recommendation) => (
                  <li>{recommendation}</li>
                ))}
              </ul>
              <hr hidden={row.errors.length === 0} />
            </div>

            <div hidden={row.errors.length === 0}>
              Y al correr los test python arrojó:
              <ul>
                {row.errors.map((error) => (
                  <li>{error}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      ),
      showExpandColumn: true,
      onlyOneExpanding: true,
    }

    return (
      <div className="unit-corrections-table">
        <h2>Unidad {unit}</h2>

        <BootstrapTable
          keyField="rowId"
          data={unitCorrections}
          columns={columns}
          expandRow={expandRow}
        />
      </div>
    )
  }

  renderUnitsAutomaticCorrections() {
    const { correctionsFetchError, corrections } = this.state
    if (correctionsFetchError) {
      return (
        <div className="app-submit-error-msg">
          Hubo un problema al cargar tus correcciones automáticas. Por favor
          intentalo mas tarde.
        </div>
      )
    }
    if (!corrections) {
      return <div>No hay correcciones automáticas disponibles.</div>
    }
    const units = this.unitsReader.listUnits()
    return units.map(this.renderCorrections)
  }

  render() {
    const { correctionsLoading } = this.state
    return correctionsLoading ? (
      <Spinner />
    ) : (
      this.renderUnitsAutomaticCorrections()
    )
  }
}
