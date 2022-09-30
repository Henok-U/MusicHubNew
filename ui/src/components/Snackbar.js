import {useSnackbar} from 'notistack'
import { Button } from "@mui/material";

export function UseSnackbarQueue(variant) {

    const {enqueueSnackbar, closeSnackbar} = useSnackbar();
    const action = snackbarId => (
      <>
        <Button onClick={() => { closeSnackbar(snackbarId) }} style={{color: 'white'}}>
           Dismiss
        </Button>
      </>
    )
  return (message)=> {
    enqueueSnackbar(message,
        {
            variant,
            anchorOrigin:{
                vertical: 'bottom',
                horizontal: 'left'
            },
            action: action,
            autoHideDuration: 4000
        })
  }
}

export default UseSnackbarQueue