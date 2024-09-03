import React from 'react';
import '../../styles/Popup.css';

// displayed on form submission 
class Popup extends React.Component {
  render() {
    const { bus_line, bus_stop, start_time, end_time, email, onClose } = this.props;

    return (
      <div className="popup">
        <div className="popup-inner">
          <h2>Scheduled successfully</h2>
          <p><strong>Bus line:</strong> {bus_line}</p>
          <p><strong>Bus stop:</strong> {bus_stop}</p>
          <p><strong>Interval start time:</strong> {start_time}</p>
          <p><strong>Interval end time:</strong> {end_time}</p>
          <p><strong>E-mail:</strong> {email}</p>
          <button className="close-btn" onClick={onClose}>X</button>
        </div>
      </div>
    );
  }
}

export default Popup;
