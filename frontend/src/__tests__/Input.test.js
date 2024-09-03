import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import Input from '../assets/components/Input';

describe('Input Component', () => {
  const mockHandleChange = jest.fn();
  const mockHandleSubmit = jest.fn();
  const mockFormData = {
    bus_line: '',
    bus_stop: '',
    email: '',
  };
  const mockStops = [{ stop_name: 'Stop 1' }, { stop_name: 'Stop 2' }];

  beforeEach(() => {
    render(
      <Input
        formData={mockFormData}
        handleChange={mockHandleChange}
        handleSubmit={mockHandleSubmit}
        stops={mockStops}
      />
    );
  });

  test('renders form elements', () => {
    expect(screen.getByLabelText(/Linha do Ônibus/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Ponto de Ônibus/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Intervalo de horário para Partida \(Início\)/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/E-mail/i)).toBeInTheDocument();
  });

  test('button should be disabled if form is incomplete', () => {
    const submitButton = screen.getByText('Agendar');
    expect(submitButton).toBeDisabled();
  });

  test('calls handleChange on input change', () => {
    fireEvent.change(screen.getByPlaceholderText('Ex.: 565'), {
      target: { value: '123' },
    });
    expect(mockHandleChange).toHaveBeenCalled();
  });

  test('submits the form and shows the popup', () => {
    fireEvent.change(screen.getByPlaceholderText('Ex.: 565'), {
      target: { value: '123' },
    });
    fireEvent.change(screen.getByPlaceholderText('email@example.com'), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByPlaceholderText('Ex.: 08:10:00'), {
      target: { value: '081000' },
    });
    fireEvent.change(screen.getByPlaceholderText('Ex.: 08:20:00'), {
      target: { value: '082000' },
    });
    fireEvent.change(screen.getByLabelText(/Ponto de Ônibus/i), {
      target: { value: 'Stop 1' },
    });

    const submitButton = screen.getByText('Agendar');
    expect(submitButton).not.toBeDisabled();

    fireEvent.click(submitButton);
    expect(mockHandleSubmit).toHaveBeenCalled();
  });

  test('clears the form fields when the "Limpar componentes" button is clicked', () => {
    fireEvent.change(screen.getByPlaceholderText('Ex.: 565'), {
      target: { value: '123' },
    });

    const clearButton = screen.getByText('Limpar componentes');
    fireEvent.click(clearButton);

    expect(screen.getByPlaceholderText('Ex.: 565').value).toBe('');
  });
});
