import { Routes, Route } from "react-router-dom";

import { AdminRoute, AuthProvider } from "./pages/auth/AuthContext";
import HomePage from "./pages/General/HomePage";
import ResgisterPage from "./pages/auth/ResgisterPage";
import LoginPage from "./pages/auth/LoginPage";
import ProfilePage from "./pages/General/ProfilePage";
import DepartmentPage from "./pages/admin/DepartmentsPage";
import LevelPage from "./pages/admin/LevelsPage";
import UserPage from "./pages/admin/Users/UsersPage";

function App() {
  return(
    <AuthProvider>
      <Routes>  
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<ResgisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />

        {/* --------------------- ADMIN ROUTES --------------------- */}
        <Route path="/departments" element={

          <AdminRoute>
            <DepartmentPage />
          </AdminRoute>}
        />

        <Route path="/levels" element={
          <AdminRoute>
            <LevelPage />
          </AdminRoute>}
        />

        <Route path="/users" element={
          <AdminRoute>
            <UserPage />
          </AdminRoute>}
        />

      </Routes>
    </AuthProvider>
  );
}

export default App;
