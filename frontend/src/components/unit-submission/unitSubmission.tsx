import * as React from 'react'
import { Accordion, Alert, Button, Form } from 'react-bootstrap'
import { UnitsReader } from '../../units/unitsReader'
import { CourseApi } from '../../remote-api/courseApi'
import { Props, State } from './types'
import {
  QuestionData,
  SelfEvaluationResponseOptions,
} from '../../remote-api/types'
import { earlyThanToday } from '../../helpers/DateHelper'
import Spinner from '../spinner/spinner'
import {
  logEvaluation, logEvaluationError,
  logEvaluationQuestions,
  logEvaluationQuestionsError
} from "../../GAEventsHandler"

export default class UnitSubmission extends React.Component<Props, State> {
  ACCEPTS_PAIR_REVIEW = 'acceptsPairReview'
  PAIR_REVIEW_COMMENT = 'pairReviewComment'
  SUCCESS_STATUS = 'success'
  ERROR_STATUS = 'error'

  private unitsReader: UnitsReader
  private exercises: string[]
  private isOverDue: boolean
  private courseApi: CourseApi

  constructor(props: Props) {
    super(props)
    this.courseApi = new CourseApi()
    this.unitsReader = new UnitsReader()
    const unitDetails = this.unitsReader.unitDetails(props.unit)
    this.exercises = unitDetails.exercises
    this.isOverDue = earlyThanToday(unitDetails.dueDate)
    this.state = { questionsLoading: false, submissionStatus: '' }
  }

  componentDidMount() {
    const { unit } = this.props
    this.setState({ questionsLoading: true })
    this.courseApi
      .selfEvaluationQuestions(unit)
      .then((response) => {
        if (!!response && response.isSuccessful()) {
          logEvaluationQuestions()
          this.setState({ questions: response.data(), questionsLoading: false })
        } else {
          logEvaluationQuestionsError()
          this.setState({
            questions: undefined,
            questionsLoading: false,
            selfEvaluationCompleted: true,
          })
        }
      })
      .catch(() => {
        logEvaluationQuestionsError()
        this.setState({ questions: undefined, questionsLoading: false })
      })
  }

  handleOptionOnChange = (questionKey: string) => (event: any) => {
    this.setState({
      [questionKey]: event.target.selectedOptions[0].id,
    })
  }

  handleExerciseOptionOnChange =
    (questionKey: string, exercise: string) => (event: any) => {
      const options = this.state[questionKey]
      this.setState({
        [questionKey]: {
          ...options,
          [exercise]: event.target.selectedOptions[0].id,
        },
      })
    }

  handleBooleanOptionOnChange = (questionKey: string) => (event: any) => {
    const id = event.target.selectedOptions[0].id
    this.setState({
      [questionKey]: id,
    })
  }

  handleValueOnChange = (questionKey: string) => (event: any) => {
    this.setState({
      [questionKey]: event.target.value,
    })
  }

  handleNumberValueOnChange = (questionKey: string) => (event: any) => {
    const value = event.target.value
    this.setState({
      [questionKey]: value,
    })
  }

  handleOnExerciseChange = (questionKey: string) => (event: any) => {
    const { fileExercises } = this.state
    this.setState({
      fileExercises: {
        ...fileExercises,
        [questionKey]: event.target.files[0],
      },
    })
  }

  selfEvaluationResults = (): { [key: string]: string } => {
    const { questions } = this.state
    const evaluationResults: { [key: string]: string } = {}
    if (questions) {
      const questionKeys = Object.keys(questions)
      questionKeys.forEach((key) => {
        const result = this.state[key]
        if (result) evaluationResults[key] = result
      })
    }
    return evaluationResults
  }

  handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    event.stopPropagation()

    const { unit } = this.props
    const { fileExercises, acceptsPairReview, pairReviewComment } = this.state
    const evaluationResults = this.selfEvaluationResults()
    this.courseApi
      .unitSubmission(
        Number(unit),
        fileExercises,
        acceptsPairReview,
        pairReviewComment,
        evaluationResults
      )
      .then((ignore) => {
        logEvaluation()
        this.setState({ submissionStatus: this.SUCCESS_STATUS })
      })
      .catch((ignore) => {
        logEvaluationError()
        this.setState({ submissionStatus: this.ERROR_STATUS })
      })
  }

  renderExerciseField = (exercise: string) => {
    return (
      <Form.Group className="mb-3" controlId={'exercise-' + exercise}>
        <Form.Label>{exercise}</Form.Label>
        <Form.Control
          type="file"
          onChange={this.handleOnExerciseChange(exercise)}
        />
      </Form.Group>
    )
  }

  renderStringQuestion = (questionKey: string, questionData: QuestionData) => {
    return (
      <Form.Group className="mb-3" controlId="formStringResponse">
        <Form.Label>{questionData.question}</Form.Label>
        <Form.Control
          required={!this.state.selfEvaluationCompleted}
          onChange={this.handleValueOnChange(questionKey)}
          id={questionKey}
        />
      </Form.Group>
    )
  }

  renderNumberQuestion = (questionKey: string, questionData: QuestionData) => {
    return (
      <Form.Group className="mb-3" controlId="formNumberResponse">
        <Form.Label>{questionData.question}</Form.Label>
        <Form.Control
          min="0"
          type="number"
          required={!this.state.selfEvaluationCompleted}
          onChange={this.handleNumberValueOnChange(questionKey)}
          id={questionKey}
        />
      </Form.Group>
    )
  }

  renderOptionsQuestion = (questionKey: string, questionData: QuestionData) => {
    const responses = questionData.responses as SelfEvaluationResponseOptions
    const responseKeys = Object.keys(responses)

    const renderExerciseEvaluation = () => {
      return this.exercises.map((exercise) => {
        return (
          <div className="mb-3 ms-3">
            <Form.Label>{exercise}</Form.Label>
            <div>
              {renderEvaluation(
                this.handleExerciseOptionOnChange(questionKey, exercise)
              )}
            </div>
          </div>
        )
      })
    }

    const renderEvaluation = (onChange: any) => {
      return (
        <Form.Select
          required={!this.state.selfEvaluationCompleted}
          onChange={onChange}
        >
          <option value="" />
          {responseKeys.map((key) => (
            <option value={responses[key]} id={key}>
              {responses[key]}
            </option>
          ))}
        </Form.Select>
      )
    }

    return (
      <Form.Group className="mb-3" controlId="formOptionsResponse">
        <Form.Label>{questionData.question}</Form.Label>

        {questionData.is_exercise_evaluation
          ? renderExerciseEvaluation()
          : renderEvaluation(this.handleOptionOnChange(questionKey))}
      </Form.Group>
    )
  }

  renderQuestions = () => {
    const { questions } = this.state
    if (!questions)
      return (
        <div className="app-submit-error-msg">
          Hubo un problema al cargar las preguntas. Por favor, volvé a
          intentarlo mas tarde.
        </div>
      )

    return Object.keys(questions).map((questionKey) => {
      const questionData = questions[questionKey]
      switch (questionData.responses) {
        case 'String':
          return this.renderStringQuestion(questionKey, questionData)
        case 'Integer':
          return this.renderNumberQuestion(questionKey, questionData)
        default:
          return this.renderOptionsQuestion(questionKey, questionData)
      }
    })
  }

  renderExercisesSolutionsSection(collapse: boolean) {
    return (
      <Accordion defaultActiveKey={collapse ? '' : '0'} className="mb-3">
        <Accordion.Item eventKey="0">
          <Accordion.Header>Soluciones</Accordion.Header>
          <Accordion.Body>
            {this.exercises.map(this.renderExerciseField)}
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    )
  }

  renderPairReviewSection(collapse: boolean) {
    const { selfEvaluationCompleted, acceptsPairReview } = this.state
    return (
      <Accordion defaultActiveKey={collapse ? '' : '0'} className="mb-3">
        <Accordion.Item eventKey="0" hidden={selfEvaluationCompleted}>
          <Accordion.Header>Correcciones entre pares</Accordion.Header>
          <Accordion.Body>
            Mirar y comprender código ajeno es una gran forma de aprender
            distintas formas de programar. Por eso te invitamos a participar en
            esta revisión ciega con tus compañeres. Para participar tenés que
            mandar el ejercicio informe.py para que revisen y comprometerte
            durante la próxima semana a revisar el código de otre.
            <Form.Group className="mb-3" controlId="peerReviewCheck">
              <Form.Label>¿Participás esta semana?</Form.Label>
              <Form.Select
                required={!selfEvaluationCompleted}
                onChange={this.handleBooleanOptionOnChange(
                  this.ACCEPTS_PAIR_REVIEW
                )}
              >
                <option value="" />
                <option id="true">Sí</option>
                <option id="false">No</option>
              </Form.Select>
            </Form.Group>
            <Form.Group
              className="mb-3"
              controlId="peerReviewComment"
              hidden={acceptsPairReview !== 'true'}
            >
              <Form.Label>
                ¿Querés dejarle un comentario a tu compañere?
              </Form.Label>
              <Form.Control
                onChange={this.handleValueOnChange(this.PAIR_REVIEW_COMMENT)}
                id={this.PAIR_REVIEW_COMMENT}
              />
            </Form.Group>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    )
  }

  renderQuestionsSection(collapse: boolean) {
    const { selfEvaluationCompleted, questionsLoading } = this.state
    return (
      <Accordion defaultActiveKey={collapse ? '' : '0'} className="mb-3">
        <Accordion.Item eventKey="0" hidden={selfEvaluationCompleted}>
          <Accordion.Header>Evaluación</Accordion.Header>
          <Accordion.Body>
            {questionsLoading ? <Spinner /> : this.renderQuestions()}
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    )
  }

  renderSubmissionMsg() {
    const { submissionStatus } = this.state
    if (submissionStatus === this.ERROR_STATUS) {
      return (
        <div className="app-submit-error-msg">
          <span>
            Ocurrió un error al enviar tus respuestas. Por favor, volvé a
            intentarlo mas tarde.
          </span>
        </div>
      )
    }
    if (submissionStatus === this.SUCCESS_STATUS) {
      return (
        <div className="app-submit-success-msg">
          <span>Tus respuestas fueron enviadas con éxito!</span>
        </div>
      )
    }
  }

  render() {
    const { unit } = this.props
    const { submissionStatus } = this.state
    const unitSubmitted = submissionStatus === this.SUCCESS_STATUS

    return (
      <div className="content">
        <h2 className="app-form-header">
          Formulario de entrega de la unidad {unit}
        </h2>

        {this.isOverDue && (
          <Alert variant="warning">
            La fecha de entrega de esta unidad ya terminó
          </Alert>
        )}

        <Form onSubmit={this.handleSubmit}>
          {this.renderExercisesSolutionsSection(unitSubmitted)}
          {this.renderPairReviewSection(unitSubmitted)}
          {this.renderQuestionsSection(unitSubmitted)}

          <Button
            variant="primary"
            type="submit"
            className="unit-submit"
            data-testid="submit"
            disabled={unitSubmitted}
          >
            Entregar unidad
          </Button>

          {this.renderSubmissionMsg()}
        </Form>
      </div>
    )
  }
}
