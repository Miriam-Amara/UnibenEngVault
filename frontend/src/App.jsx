import { Routes, Route } from "react-router-dom";
import Register from "./pages/auth/Register.jsx";
import Users from "./pages/admin/Users.jsx"

function App() {
  return(
    <Routes>
      <Route path="/register" element={<Register />}></Route>
      <Route path="/users" element={<Users />}></Route>
    </Routes>
  );
}

export default App
