import { Routes, Route } from "react-router-dom";
import CoursesPage from "./pages/admin/CoursesPage.jsx";
import DepartmentPage from "./pages/admin/Departments.jsx";
import LevelPage from "./pages/admin/Levels.jsx";
import Login from "./pages/auth/Login.jsx";
import Register from "./pages/auth/Register.jsx";
import UsersPage from "./pages/admin/Users.jsx"

function App() {
  return(
    <Routes>
      <Route path="/departments" element={<DepartmentPage />} />
      <Route path="/courses" element={<CoursesPage />} />
      <Route path="/levels" element={<LevelPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/users" element={<UsersPage />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;
