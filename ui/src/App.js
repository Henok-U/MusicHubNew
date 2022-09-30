import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home"
import Register from "./pages/Register"
function App() {
  return (
    <Router basename="/">
    <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register/" element={<Register />} />
    </Routes>
  </Router>
  );
}

export default App;
