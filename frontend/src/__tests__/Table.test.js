import React from 'react';
import { render, screen } from '@testing-library/react';
import Table from '../assets/components/Table';

describe('Table Component', () => {
  const mockData = [
    { ordem: 'Bus 1', velocidade: 60, distancia: 10 },
    { ordem: 'Bus 2', velocidade: 50, distancia: 20 },
  ];

  beforeEach(() => {
    render(<Table data={mockData} />);
  });

  test('renders table headers', () => {
    expect(screen.getByText(/Ônibus/i)).toBeInTheDocument();
    expect(screen.getByText(/Velocidade/i)).toBeInTheDocument();
    expect(screen.getByText(/Distância \(minutos\)/i)).toBeInTheDocument();
  });

  test('displays correct bus data', () => {
    expect(screen.getByText('Bus 1')).toBeInTheDocument();
    expect(screen.getByText('60')).toBeInTheDocument();
    expect(screen.getByText('10')).toBeInTheDocument();
  });
});
