import { Routes, Route } from "react-router-dom";

import HomePage from "./pages/General/HomePage";
import ResgisterPage from "./pages/auth/ResgisterPage";
import LoginPage from "./pages/auth/LoginPage";

function App() {
  return(
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/register" element={<ResgisterPage />} />
      <Route path="/login" element={<LoginPage />} />
    </Routes>
  );
}

export default App;
