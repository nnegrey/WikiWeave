import React from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import StoryWeaver from './components/StoryWeaver';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container>
        <StoryWeaver />
      </Container>
    </ThemeProvider>
  );
}

export default App;
