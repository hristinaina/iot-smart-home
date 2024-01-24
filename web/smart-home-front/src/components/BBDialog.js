import React, { useState, useEffect } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import "./Dialog.css"
import DeviceService from '../services/DeviceService';

const BBDialog = ({ open, onClose, device }) => {
  const [timeValue, setTimeValue] = useState('');
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);

  useEffect(() => {
    if (open && device) {
      if (device.value=="activated")  setIsButtonDisabled(false);
      else if (device.value="deactivated") setIsButtonDisabled(true);
      else setIsButtonDisabled(true);

      const fetchTimeData = async () => {
        let result = await DeviceService.getAlarmTime();
        if (result) {
          setTimeValue(result.time);
        }
      };
  
      if (open) {
        fetchTimeData();
      }
    }
  }, [open]);

  const handleTimeChange = (event) => {
    setTimeValue(event.target.value);
  };

  const handleTurnOff = () => {
    // todo: handle turning off logic
    console.log('Turning off...');
    onClose();
  };

  const handleSave = async () => {
    console.log('Selected time:', timeValue);
    console.log(device);
    await DeviceService.updateAlarmTime(timeValue);
    onClose();
  };

  const disabledStyles = {
    opacity: 0.5, 
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle className='dialog-title'>Alarm Clock</DialogTitle>
      <DialogContent className='alarm-dialog'>
        <TextField
          fullWidth
          type="time"
          value={timeValue}
          onChange={handleTimeChange}
        />
        <Button onClick={handleTurnOff} className="turnOffButton" disabled={isButtonDisabled} style={isButtonDisabled ? disabledStyles : {}}>
          Turn Off
        </Button>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} className="cancelButton">
          Cancel
        </Button>
        <Button onClick={handleSave} className="saveButton">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default BBDialog;
