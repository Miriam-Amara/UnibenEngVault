import axios from "axios";
import { useNavigate } from "react-router-dom";

import "./Header.css"


function Header({ menu, role }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axios.delete("/api/v1/auth_session/logout", { withCredentials: true });
      navigate("/login");
    } catch (err) {
      console.error("Logout failed:", err);
    }
  };

  return (
    <header className="header">
      <div>
        <div>{menu}</div>
        <h5>UnibenEngVault</h5>
      </div>
      <div>{role}</div>
      <div className="btn-logout">
        <button onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}

export default Header;
