import Popup from './Popup';
import axios from 'axios';
import styled from 'styled-components';
import LoadingPopup from './LoadingPopup'; 
import React, {useState, useEffect} from 'react';

const StyledButton = styled.button`
  display: inline-block;
  padding: 8px;
  font-size: 14px;
  font-family: 'SF Pro', sans-serif;
  font-weight: bold;
  color: #fff;
  background-color: ${({variant, disabled}) =>
    disabled ? '#6c757d' : variant === 'red' ? '#dc3545' : '#007bff'};
  border: none;
  border-radius: 5px;
  text-align: center;
  cursor: ${({disabled}) => (disabled ? 'not-allowed' : 'pointer')};
  width: 200px;
  height: 40px;
  transition: background-color 0.3s, transform 0.2s;

  &:hover {
    background-color: ${({variant, disabled}) =>
    disabled ? '#6c757d' : variant === 'red' ? '#c82333' : '#0056b3'};
    transform: ${({disabled}) => (disabled ? 'none' : 'translateY(-2px)')};
  }

  &:active {
    background-color: ${({variant, disabled}) =>
    disabled ? '#6c757d' : variant === 'red' ? '#bd2130' : '#00408a'};
    transform: ${({disabled}) => (disabled ? 'none' : 'translateY(0)')};
  }
`;

const ButtonContainer = styled.div`
  justify-content: center;
  align-content: center;
  display: flex;
  gap: 10px;
`;

// display inputs to fill in the information necessary for the user request
const Input = ({formData, handleChange, handleSubmit, stops}) => {
  const [start_time, setStartTime] = useState('');
  const [end_time, setEndTime] = useState('');
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);
  const [showPopup, setShowPopup] = useState(false);
  const [showLoading, setShowLoading] = useState(false); 

  useEffect(() => {
    const isFormComplete =
      formData.bus_line &&
      formData.bus_stop &&
      start_time &&
      end_time &&
      formData.email;

    setIsButtonDisabled(!isFormComplete);
  }, [formData, start_time, end_time]);

  const formatTime = (time) => {
    if (time.length > 6) time = time.slice(0, 6);
    if (time.length <= 2) return time;
    if (time.length <= 4) return time.slice(0, 2) + ':' + time.slice(2);
    return time.slice(0, 2) + ':' + time.slice(2, 4) + ':' + time.slice(4);
  };

  const handleStartTimeChange = (e) => {
    const formattedTime = formatTime(e.target.value.replace(/\D/g, ''));
    setStartTime(formattedTime);
    handleChange({target: {name: 'start_time', value: formattedTime}});
  };

  const handleEndTimeChange = (e) => {
    const formattedTime = formatTime(e.target.value.replace(/\D/g, ''));
    setEndTime(formattedTime);
    handleChange({target: {name: 'end_time', value: formattedTime}});
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    handleSubmit(e);
    setShowLoading(true);
    try {
      await registerData();
      setShowPopup(true);
    } catch (error) {
      console.error('Error sending data:', error);
    } finally {
      setShowLoading(false);
    }
  };

  const registerData = async () => {
    try {
      const response = await axios.post('http://localhost:8000/register/', {
        email: formData.email,
        bus_stop: formData.bus_stop,
        bus_line: formData.bus_line,
        start_time: start_time,
        end_time: end_time,
      });
      console.log('sending: ', response);
    } catch (error) {
      console.error('Error sending data:', error);
    }
  };

  const handleClearForm = () => {
    setStartTime('');
    setEndTime('');
    handleChange({target: {name: 'bus_line', value: ''}});
    handleChange({target: {name: 'bus_stop', value: ''}});
    handleChange({target: {name: 'start_time', value: ''}});
    handleChange({target: {name: 'end_time', value: ''}});
    handleChange({target: {name: 'email', value: ''}});
  };

  return (
    <div>
      <form
        style={{
          display: 'flex',
          flexDirection: 'column',
          maxWidth: '300px',
          margin: 'auto',
          padding: '20px',
          color: 'white',
          position: 'relative',
          fontFamily: 'SF Pro, sans-serif',
          fontWeight: 'bold',
        }}
        onSubmit={handleFormSubmit}
      >
        <label style={{marginBottom: '20px'}}>
          Bus line
          <br />
          <input
            type="text"
            name="bus_line"
            placeholder="Ex.: 565"
            value={formData.bus_line}
            onChange={handleChange}
            style={{margin: '8px 0'}}
          />
        </label>

        <label style={{marginBottom: '20px'}}>
          Bus stop
          <br />
          <select
            name="bus_stop"
            value={formData.bus_stop}
            onChange={handleChange}
            style={{margin: '8px 0', padding: '5px', width: '100%'}}
          >
            <option value="" disabled style={{color: '#767676'}}>
              Select a bus stop
            </option>
            {stops &&
              stops.map((stop, index) => (
                <option key={index} value={stop.stop_name}>
                  {stop.stop_name}
                </option>
              ))}
          </select>
        </label>

        <label style={{marginBottom: '20px'}}>
          Interval start time
          <br />
          <input
            type="text"
            placeholder="Ex.: 08:10:00"
            value={start_time}
            onChange={handleStartTimeChange}
            style={{margin: '8px 0'}}
          />
        </label>

        <label style={{marginBottom: '20px'}}>
          Interval end time
          <br />
          <input
            type="text"
            placeholder="Ex.: 09:30:00"
            value={end_time}
            onChange={handleEndTimeChange}
            style={{margin: '8px 0'}}
          />
        </label>

        <label style={{marginBottom: '20px'}}>
          E-mail
          <br />
          <input
            type="email"
            name="email"
            placeholder="E-mail adress"
            value={formData.email}
            onChange={handleChange}
            style={{margin: '8px 0'}}
          />
        </label>

        <ButtonContainer>
          <StyledButton
            type="submit"
            variant="primary"
            disabled={isButtonDisabled}
          >
            Schedule
          </StyledButton>
          <StyledButton type="button" variant="red" onClick={handleClearForm}>
           Clean components
          </StyledButton>
        </ButtonContainer>
      </form>

      {showPopup && (
        <Popup
          title="success"
          bus_line={formData.bus_line}
          bus_stop={formData.bus_stop}
          start_time={start_time}
          end_time={end_time}
          email={formData.email}
          onClose={() => setShowPopup(false)}
        />
      )}

      {showLoading && <LoadingPopup />}
    </div>
  );
};

export default Input;

