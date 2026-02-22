import * as React from 'react'
import { ContentReader } from '../../content/contentReader'
import { Section } from '../../content/types'
import { marked } from 'marked'
import './course.css'
import { Props, State } from './types'
import { Button } from 'react-bootstrap'
import {
  logNextContentNavigation,
  logPreviousContentNavigation,
} from '../../GAEventsHandler'

export default class Course extends React.Component<Props, State> {
  private contentReader: ContentReader

  constructor(props: Props) {
    super(props)

    this.contentReader = new ContentReader()
    this.state = { markdown: '' }

    this.renderMkd = this.renderMkd.bind(this)
    this.handlePreviousClick = this.handlePreviousClick.bind(this)
    this.handleNextClick = this.handleNextClick.bind(this)
  }

  pathFromKey(key: string, sections: Section): string | undefined {
    const path = key.split('/')[0]
    const section = sections[path]
    if (!section) return

    const filePath = section.file
    if (!!filePath) return filePath
    const nextLevelKey = key.substr(key.indexOf('/'))
    return this.pathFromKey(nextLevelKey, section)
  }

  componentWillMount() {
    const { contentPath } = this.props
    if (contentPath) {
      const { filePath, previous, next } =
        this.contentReader.filePathFrom(contentPath)
      if (!filePath) return

      fetch(filePath, { headers: { Accept: 'text/markdown' } })
        .then((response) => response.text())
        .catch((e) => {
          this.setState({ markdown: undefined, noContentAvailable: true })
        })
        .then((text) => {
          if (!text) return
          this.setState({
            markdown: marked.parse(text),
            noContentAvailable: false,
            previous,
            next,
          })
        })
        .catch((e) => {
          this.setState({ markdown: undefined, noContentAvailable: true })
        })
    }
  }

  handlePreviousClick(): void {
    const { previous } = this.state
    const { contentPath } = this.props
    logPreviousContentNavigation(contentPath, previous || '')
    window.location.href = '/programa/' + previous
  }

  handleNextClick(): void {
    const { next } = this.state
    const { contentPath } = this.props
    logNextContentNavigation(contentPath, next || '')
    window.location.href = '/programa/' + next
  }

  renderMkd() {
    const { markdown, noContentAvailable, previous, next } = this.state
    if (!markdown || noContentAvailable) return

    return (
      <div>
        <div>
          <Button
            className="float-end"
            variant="link"
            disabled={!next}
            onClick={this.handleNextClick}
          >
            Siguiente
          </Button>
          <Button
            className="float-end"
            variant="link"
            disabled={!previous}
            onClick={this.handlePreviousClick}
          >
            Anterior
          </Button>
        </div>
        <div dangerouslySetInnerHTML={{ __html: markdown }} />
      </div>
    )
  }

  render() {
    const { noContentAvailable } = this.state

    return (
      <div className="content">
        {this.renderMkd()}
        {noContentAvailable && (
          <div>La página a la que intentás acceder no existe.</div>
        )}
      </div>
    )
  }
}
