import React, { useState, useEffect } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import "./Dialog.css"

const RGBDialog = ({ open, onClose, device }) => {
  const [selectedColor, setSelectedColor] = useState('');

  useEffect(() => {
    if (open && device) {
      setSelectedColor(device.value);
    }
  }, [open]);

  const handleColorChange = (event) => {
    setSelectedColor(event.target.value);
  };

  const handleSave = () => {
    console.log('Selected color:', selectedColor);
    console.log(device);
    //todo inform back application abour the change
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle className='dialog-title'>Change Light Color</DialogTitle>
      <DialogContent className='device-dialog'>
        <FormControl fullWidth>
          <InputLabel id="color-select-label">Select Color</InputLabel>
          <Select
            labelId="color-select-label"
            id="color-select"
            value={selectedColor}
            label="Select Color"
            onChange={handleColorChange}
          >
            <MenuItem value="red">Red</MenuItem>
            <MenuItem value="green">Green</MenuItem>
            <MenuItem value="blue">Blue</MenuItem>
            <MenuItem value="lightBlue">Light Blue</MenuItem>
            <MenuItem value="yellow">Yellow</MenuItem>
            <MenuItem value="purple">Purple</MenuItem>
            <MenuItem value="white">White</MenuItem>
            <MenuItem value="off">Off</MenuItem>
          </Select>
        </FormControl>
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

export default RGBDialog;
