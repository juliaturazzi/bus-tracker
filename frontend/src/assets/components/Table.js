import React from 'react';

// display bus number, speed, and distance from chosen point
const Table = ({ data }) => {
  return (
    <div style={{ display: 'grid', justifyItems: 'center', padding: '20px' }}>
      <table style={{
        color: 'white',
        border: '2px solid white',
        borderCollapse: 'collapse',
        width: '100%',
        maxWidth: '600px',
        textAlign: 'center'
      }}>
        <thead style={{ fontSize: '22px' }}>
          <tr>
            <th style={{ padding: '10px', border: '1px solid white' }}>Bus</th>
            <th style={{ padding: '10px', border: '1px solid white' }}>Speed</th>
            <th style={{ padding: '10px', border: '1px solid white' }}>Distance (minutes)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((bus, index) => (
            <tr key={index} style={{ fontSize: '20px' }}>
              <td style={{ padding: '10px', border: '1px solid white' }}>{bus.ordem}</td>
              <td style={{ padding: '10px', border: '1px solid white' }}>{bus.velocidade}</td>
              <td style={{ padding: '10px', border: '1px solid white' }}>{bus.distancia}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;