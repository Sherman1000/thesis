import * as React from 'react'
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap'
import { ContentReader } from '../../content/contentReader'
import { Section } from '../../content/types'
import './courseNavbar.css'
import { Props, State } from './types'
import { correctionsPath } from '../../routes'
import {earlyThanToday} from "../../helpers/DateHelper"
import {logLocation} from "../../GAEventsHandler"

export default class CourseNavbar extends React.Component<Props, State> {
  private contentReader: ContentReader

  constructor(props: Props) {
    super(props)

    this.navbarSection = this.navbarSection.bind(this)
    this.navbarSectionDropdown = this.navbarSectionDropdown.bind(this)
    this.handleSelectedSection = this.handleSelectedSection.bind(this)
    this.handleLogOut = this.handleLogOut.bind(this)

    this.contentReader = new ContentReader()
  }

  navbarSectionDropdown(section: Section, title: string, path: string) {
    const subsections = Object.keys(section)
    return (
      <NavDropdown title={title} id={`${title}-nav-dropdown`}>
        {subsections.map((s) => {
          const content: Section = section[s]
          const key = `${path}/${s}`
          const isTitle = s === 'title'
          const isDate = s === 'date'
          const isAvailable = content.date ? earlyThanToday(content.date) : true
          if (isTitle || isDate || !isAvailable) return null
          if (content.file) {
            return (
              <NavDropdown.Item eventKey={key}>
                {content.title}
              </NavDropdown.Item>
            )
          } else return this.navbarSectionDropdown(content, content.title, key)
        })}
      </NavDropdown>
    )
  }

  navbarSection(section: string) {
    const sectionContent: Section =
      this.contentReader.rootSectionContent(section)
    const title = sectionContent.title
    const privateSection = sectionContent.isPrivate && !this.props.loggedUser
    const isAvailable = sectionContent.date ? earlyThanToday(sectionContent.date) : true
    if (privateSection || !isAvailable) return null
    if (sectionContent.file)
      return <Nav.Link eventKey={section}>{title}</Nav.Link>
    return this.navbarSectionDropdown(sectionContent, title, section)
  }

  handleSelectedSection(eventKey: string | null) {
    if (eventKey) {
      logLocation()
      window.location.href = "/programa/" + eventKey
    }
  }

  handleLogOut() {
    this.props.logoutUser()
  }

  render() {
    const { loggedUser } = this.props
    return (
      <Navbar bg="light" expand="xxl">
        <Container className="navbar-container">
          <Navbar.Brand>Programación en Python</Navbar.Brand>
          <Nav
            className="me-auto"
            onSelect={this.handleSelectedSection}
            hidden={!loggedUser}
          >
            {this.contentReader.rootSections.map(this.navbarSection)}
            <Nav.Link href={correctionsPath} hidden={!loggedUser}>
              Mis entregas y correcciones
            </Nav.Link>
          </Nav>

          <Nav.Link onClick={this.handleLogOut} className="justify-content-end" hidden={!loggedUser}>
            Cerrar sesión
          </Nav.Link>
        </Container>
      </Navbar>
    )
  }
}
