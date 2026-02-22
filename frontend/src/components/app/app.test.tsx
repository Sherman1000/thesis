import { render } from '@testing-library/react'
import App from './app'

test('renders App component', () => {
  const { container } = render(<App />)
  expect(container).not.toBeNull()
})
