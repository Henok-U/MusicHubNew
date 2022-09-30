import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home"
import Register from "./pages/Register"
import SignIn from "./pages/SignIn"
function App() {
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
