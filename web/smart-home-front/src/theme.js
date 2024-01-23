import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#c9b48d',
    },
    secondary: {
      main: '#47454a',
    },
  },
  customStyles: {
    myCustomButton: {
      textTransform: 'none',
      fontFamily: 'Poppins',
      width: '37%',
    },
    // Add more custom styles as needed
  },
});

export default theme;
