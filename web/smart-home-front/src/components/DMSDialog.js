import React, { useState, useEffect } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import "./Dialog.css"

const DMSDialog = ({ open, onClose, device }) => {
  const [inputValue, setInputValue] = useState('');


  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSave = () => {
    console.log('Input value:', inputValue);
    console.log(device);
    // todo: inform back application about the change
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle className='dialog-title'>Enter PIN</DialogTitle>
      <DialogContent className='device-dialog'>
        <TextField
          fullWidth
          label="Enter PIN"
          value={inputValue}
          onChange={handleInputChange}
        />
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

export default DMSDialog;
