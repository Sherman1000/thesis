import * as React from 'react'
import { Props, State } from './types'
import { Spinner as BootstrapSpinner} from 'react-bootstrap'

export default class Spinner extends React.Component<Props, State> {
  render() {
    return (
      <BootstrapSpinner animation="border" role="status">
        <span className="visually-hidden">{this.props.message || 'Cargando...'}</span>
      </BootstrapSpinner>
    )
  }
}
