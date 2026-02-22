import * as React from 'react'
import { Props, State } from './types'
import { UnitsReader } from '../../units/unitsReader'
import { CourseApi } from '../../remote-api/courseApi'
import {
  CorrectionsByUnit,
  UnitCorrection,
  UnitsCorrections,
} from '../../remote-api/types'
import Spinner from '../spinner/spinner'
import BootstrapTable from 'react-bootstrap-table-next'
import './teacherCorrections.css'
import { logCorrections, logCorrectionsError } from '../../GAEventsHandler'

export default class TeacherCorrections extends React.Component<Props, State> {
  private unitsReader: UnitsReader
  private courseApi: CourseApi

  constructor(props: Props) {
    super(props)
    this.unitsReader = new UnitsReader()
    this.courseApi = new CourseApi()
    this.state = { correctionsLoading: false, correctionsFetchError: false }
    this.renderUnitCorrections = this.renderUnitCorrections.bind(this)
    this.updateStateWithCorrections = this.updateStateWithCorrections.bind(this)
  }

  orderCorrectionsByUnit(
    corrections: UnitsCorrections | undefined
  ): CorrectionsByUnit | undefined {
    if (!corrections || corrections.length === 0) return

    const orderedCorrections: CorrectionsByUnit = {}
    corrections.forEach((correction: UnitCorrection) => {
      const unit = correction.unit.toString()
      const processedCorrections = orderedCorrections[unit] || []
      debugger
      processedCorrections.push({
        exercise: correction.exercise,
        reviewer: correction.reviewer,
        exercise_solution: correction.exercise_solution,
        correction: correction.correction,
        datetime: correction.datetime,
      })
      orderedCorrections[unit] = processedCorrections
    })
    return orderedCorrections
  }

  updateStateWithCorrections(corrections?: CorrectionsByUnit) {
    this.setState({
      corrections: corrections,
      correctionsLoading: false,
      correctionsFetchError: !corrections,
    })
  }

  fetchUnitsCorrections(userId: string = '') {
    if (!userId) {
      return
    }
    this.setState({ correctionsLoading: true })
    this.courseApi
      .unitsCorrections(userId)
      .then((response) => {
          debugger
        if (!!response && response.isSuccessful()) {
          logCorrections()
          const corrections = this.orderCorrectionsByUnit(response.data())
          corrections && this.props.onCorrectionsLoad()
          this.updateStateWithCorrections(corrections)
        } else {
          logCorrectionsError()
          this.updateStateWithCorrections()
        }
      })
      .catch(() => {
        logCorrectionsError()
        this.updateStateWithCorrections()
      })
  }

  componentWillReceiveProps(nextProps: Props) {
    if (nextProps.selectedStudent !== this.props.selectedStudent) {
      this.fetchUnitsCorrections(nextProps.selectedStudent)
    }
  }

  componentDidMount() {
    const { selectedStudent } = this.props
    this.fetchUnitsCorrections(selectedStudent)
  }

  renderUnitCorrections(unit: string) {
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
        text: 'Ejercicio',
      },
      {
        dataField: 'exercise_solution',
        text: 'Archivo entregado',
        formatter: (editorProps: any, value: any) => (
          <div dangerouslySetInnerHTML={{ __html: value.exercise_solution }} />
        ),
      },
      {
        dataField: 'reviewer',
        text: 'Correctxr',
      },
    ]

    const expandRow = {
      renderer: (row: any) => (
        <div>
          <h4>Corrección</h4>
          <div className="teacher-corrections">{row.correction}</div>
        </div>
      ),
      showExpandColumn: true,
      onlyOneExpanding: true,
    }

    return (
      <div className="unit-corrections-table">
        <h2>Unidad {unit}</h2>
        <BootstrapTable
          keyField="exercise"
          data={unitCorrections}
          columns={columns}
          expandRow={expandRow}
        />
      </div>
    )
  }

  renderUnitsCorrections() {
    const { correctionsFetchError, corrections } = this.state
    if (correctionsFetchError) {
      return (
        <div className="app-submit-error-msg">
          Hubo un problema al cargar tus correcciones. Por favor intentalo mas
          tarde.
        </div>
      )
    }
    if (!corrections) {
      return <div>No hay correcciones disponibles.</div>
    }
    const units = this.unitsReader.listUnits()
    return units.map(this.renderUnitCorrections)
  }

  render() {
    const { correctionsLoading } = this.state
    return correctionsLoading ? <Spinner /> : this.renderUnitsCorrections()
  }
}
