import { Routes, Route } from "react-router-dom";

import { AdminRoute, AuthProvider } from "./pages/auth/AuthContext";
import HomePage from "./pages/General/HomePage";
import ResgisterPage from "./pages/auth/ResgisterPage";
import LoginPage from "./pages/auth/LoginPage";
import ProfilePage from "./pages/General/ProfilePage";

function App() {
  return(
    <AuthProvider>
      <Routes>  
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<ResgisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
