import axios from "axios";
import { useNavigate } from "react-router-dom";

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
    <header>
      <div>{menu}</div>
      <h3>UnibenEngVault</h3>
      <div>{role}</div>
      <div>
        <button onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}

export default Header;
