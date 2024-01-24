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
import DeviceService from '../services/DeviceService';
import "./Dialog.css"

const RGBDialog = ({ open, onClose, device }) => {
  const [selectedColor, setSelectedColor] = useState('');

  useEffect(() => {
    if (open && device) {
      const colorMapping = {
        'red': 1,
        'green': 2,
        'blue': 3,
        'lightBlue': 5,
        'yellow': 4,
        'purple': 6,
        'white': 7,
        'off': 0,
      };
      setSelectedColor(colorMapping[device.value]);
    }
  }, [open]);

  const handleColorChange = (event) => {
    setSelectedColor(event.target.value);
  };

  const handleSave = async () => {
    try {
      const result = await DeviceService.updateRGBLight(selectedColor);
  } catch (error) {
      console.log("Error fetching data from the server");
      console.log(error);
  }
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
            <MenuItem value="1">Red</MenuItem>
            <MenuItem value="2">Green</MenuItem>
            <MenuItem value="3">Blue</MenuItem>
            <MenuItem value="5">Light Blue</MenuItem>
            <MenuItem value="4">Yellow</MenuItem>
            <MenuItem value="6">Purple</MenuItem>
            <MenuItem value="7">White</MenuItem>
            <MenuItem value="0">Off</MenuItem>
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
