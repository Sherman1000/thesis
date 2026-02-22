import { render, screen } from '@testing-library/react'
import Login from './login'

describe('Login component', () => {
  let container: any

  describe('Basic component', () => {
    const loginUser = () => {}

    beforeEach(() => {
      container = render(<Login loginUser={loginUser} />).container
    })

    test('renders header', () => {
      expect(container.querySelector('.app-form')).toBeDefined()
      expect(container.querySelector('.app-form-header').innerText).toBe(
        'Bienvenidx!'
      )
    })

    test('renders form fields', () => {
      expect(container.querySelector('.app-form')).toBeDefined()
      expect(container.querySelector('[controlId="formEmail"]')).toBeDefined()
      expect(
        container.querySelector('[controlId="formPassword"]')
      ).toBeDefined()
      expect(container.querySelector('[type="submit"]')).toBeDefined()
      expect(
        container.querySelector('.app-submit-error-msg')
      ).toBeUndefined()
    })
  })

  describe('Basic component', () => {
    const loginUser = () => {}

    beforeEach(() => {
      container = render(
        <Login loginUser={loginUser} accessError={true} />
      ).container
    })

    test('renders form fields', () => {
      expect(
        container.querySelector('.app-submit-error-msg')).toBeDefined()
    })
  })
})
