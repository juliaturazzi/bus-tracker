import React from 'react';
import { render, screen, fireEvent} from '@testing-library/react';
import Popup from '../assets/components/Popup';

describe('Popup Component', () => {
  const mockOnClose = jest.fn();
  const mockProps = {
    bus_line: '123',
    bus_stop: 'Stop 1',
    start_time: '08:10:00',
    end_time: '08:20:00',
    email: 'test@example.com',
    onClose: mockOnClose,
  };

  beforeEach(() => {
    render(<Popup {...mockProps} />);
  });

  test('renders popup with correct details', () => {
    expect(screen.getByText(/Linha do Ônibus:/i)).toHaveTextContent('123'); 
    expect(screen.getByText(/Ponto de Ônibus:/i)).toHaveTextContent('Stop 1');
    expect(screen.getByText(/Horário de Início:/i)).toHaveTextContent('08:10:00');
    expect(screen.getByText(/E-mail:/i)).toHaveTextContent('test@example.com');
  });

  test('calls onClose when close button is clicked', () => {
    fireEvent.click(screen.getByText('X'));
    expect(mockOnClose).toHaveBeenCalled();
  });
});
