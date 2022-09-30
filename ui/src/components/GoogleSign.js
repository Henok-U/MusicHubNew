import React, { useState } from "react";
import {useNavigate} from 'react-router-dom'
import { GoogleLogin } from "react-google-login";
import axios from "../Axios";
import { UseSnackbarQueue } from "../components/Snackbar";
const clientId = process.env.REACT_APP_GOOGLE_API_KEY;

export default function GoogleSign() {
  const [loading, setLoading] = useState("Loading...");
  const navigate = useNavigate();
  const showSuccess = UseSnackbarQueue("success");
  const showError = UseSnackbarQueue("error");

  const handleLoginSuccess = (response) => {
    const json = JSON.stringify({
      access_token: response.accessToken,
    });
    axios
        .post("user/signin-social/google-oauth2/", json, {
            headers: {
              "Content-Type": "application/json"
          }
      })
      .then((res) => {
        showSuccess("Successful Signin!");
        sessionStorage.setItem("token", res.data.token);
        navigate("/");
      })
      .catch((err) => {
        showError(err.response.data.message);
      });

    setLoading();
  };

  const handleLoginFailure = (error) => {
    console.log("Login Failure ", error);
    setLoading();
  };

  const handleRequest = () => {
    setLoading("Loading...");
  };

  const handleAutoLoadFinished = () => {
    setLoading();
  };

  return (
    <GoogleLogin
      clientId={clientId}
      buttonText={loading}
      onSuccess={handleLoginSuccess}
      onFailure={handleLoginFailure}
      onRequest={handleRequest}
      onAutoLoadFinished={handleAutoLoadFinished}
    />
  );
}
