import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Link from '@mui/material/Link'
export default function ButtonAppBar() {


  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>

          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            <Link underline="none" href="/">MusicHub</Link>
          </Typography>

          <Link underline="none" href="/login/">
            <Button variant="contained" color="inherit" >Login</Button>
          </Link>

          {/* <Link underline="none" href="/register/"> */}
          <Button href="/register/" variant="contained" color="inherit" >Register</Button>
          {/* </Link> */}

        </Toolbar>
      </AppBar>
    </Box >
  );
}
