import { Routes, Route } from "react-router-dom";
import CoursesPage from "./pages/admin/CoursesPage.jsx";
import DashboardPage from "./pages/admin/Dashboard.jsx";
import DepartmentPage from "./pages/admin/Departments.jsx";
import FilesPage from "./pages/admin/Files.jsx";
import LevelPage from "./pages/admin/Levels.jsx";
import Login from "./pages/auth/Login.jsx";
import Register from "./pages/auth/Register.jsx";
import UsersPage from "./pages/admin/Users.jsx"

function App() {
  return(
    <Routes>
      <Route path="/courses" element={<CoursesPage />} />
      <Route path="/admins/dashboard" element={<DashboardPage />} />
      <Route path="/departments" element={<DepartmentPage />} />
      <Route path="/files" element={<FilesPage />} />
      <Route path="/levels" element={<LevelPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/users" element={<UsersPage />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;
