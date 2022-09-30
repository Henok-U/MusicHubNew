import React from "react";
import ReactDOM from "react-dom/client";
import "./css/index.css";
import App from "./App";
import {SnackbarProvider} from 'notistack'
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <SnackbarProvider maxSnack={3}>
      <App />
    </SnackbarProvider>
  </React.StrictMode>
);
