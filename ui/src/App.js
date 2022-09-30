import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home"
import Register from "./pages/Register"
import SignIn from "./pages/SignIn"
import { gapi } from "gapi-script";
function App() {
  gapi.load("client:auth2", () => {
    gapi.client.init({
      clientId: process.env.REACT_APP_GOOGLE_API_KEY,
      plugin_name: "chat",
    });
  });
  return (
    <Router basename="/">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register/" element={<Register />} />
        <Route path="/login/" element={<SignIn />} />
      </Routes>
    </Router>
  );
}

export default App;
