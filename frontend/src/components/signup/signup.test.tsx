import {fireEvent, render} from '@testing-library/react';
import Signup from './signup'

describe('Signup component', () => {
  const signUpUser = jest.fn()
  const defaultProps = {
    signUpUser,
    hash: 'some-hash'
  }

  test('renders signup form fields', () => {
    const {container} = render(<Signup {...defaultProps}/>)
    expect(container.querySelector('.signup')).not.toBeNull();
    expect(container.querySelector('.signup-header').innerHTML).toEqual('Bienvenidx!');
    expect(container.querySelector('.signup-email')).not.toBeNull();
    expect(container.querySelector('.signup-password')).not.toBeNull();
    expect(container.querySelector('.signup-confirmation-password')).not.toBeNull();
    expect(container.querySelector('.signup-submit')).not.toBeNull();
    expect(container.querySelector('.submit-error')).toBeNull();
    expect(container.querySelector('.login-msg')).not.toBeNull();
  });

  test('renders signup form fields and error msg', () => {
    const {container} = render(<Signup {...defaultProps} creationError={true}/>)
    expect(container.querySelector('.signup')).not.toBeNull();
    expect(container.querySelector('.signup-header').innerHTML).toEqual('Bienvenidx!');
    expect(container.querySelector('.signup-email')).not.toBeNull();
    expect(container.querySelector('.signup-password')).not.toBeNull();
    expect(container.querySelector('.signup-confirmation-password')).not.toBeNull();
    expect(container.querySelector('.signup-submit')).not.toBeNull();
    expect(container.querySelector('.submit-error')).not.toBeNull();
    expect(container.querySelector('.login-msg')).not.toBeNull();
  });

  test('calls signUpUser prop on submit', () => {
    const {getByPlaceholderText, getByText} = render(<Signup {...defaultProps}/>)
    const emailInput = getByPlaceholderText(/Email/i);
    const passwordInput = getByPlaceholderText(/Contraseña/i);
    const confirmationPasswordInput = getByPlaceholderText(/Repetí contraseña/i);

    fireEvent.change(emailInput, {target: {value: 'email@test.com'}});
    fireEvent.change(passwordInput, {target: {value: 'thisIsMyPassword'}});
    fireEvent.change(confirmationPasswordInput, {target: {value: 'thisIsMyPassword'}});
    fireEvent.click(getByText(/Crear cuenta/i));

    expect(signUpUser).toHaveBeenCalledWith('some-hash', 'email@test.com', 'thisIsMyPassword', 'thisIsMyPassword');
  });

  test('does not call signUpUser prop on submit if invalid fields', () => {
    const {getByPlaceholderText, getByText} = render(<Signup {...defaultProps}/>)
    const emailInput = getByPlaceholderText(/Email/i);
    const passwordInput = getByPlaceholderText(/Contraseña/i);
    const confirmationPasswordInput = getByPlaceholderText(/Repetí contraseña/i);

    fireEvent.change(emailInput, {target: {value: 'email@test.com'}});
    fireEvent.change(passwordInput, {target: {value: 'short'}});
    fireEvent.change(confirmationPasswordInput, {target: {value: 'short'}});
    fireEvent.click(getByText(/Crear cuenta/i));

    expect(signUpUser).not.toHaveBeenCalled();
  });
});



