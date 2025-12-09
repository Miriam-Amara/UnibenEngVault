/**
 * 
 */


import { useNavigate } from "react-router-dom";

import { logoutApi } from "../../api/users";
import { useAuth } from "../../pages/auth/AuthContext";
import { Button } from "../ui/Button";
import sidebarIcon from "../../assets/sidebar_menu_icon.png";



export default function Header({
  showSidebar,
  setShowSidebar,
  className
}) {

  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const handleLogout = async () => {
    try {
      await logoutApi();

      logout();
      navigate("/login");
      
    } catch (error) {
      console.error("Error in logout: ", error)
    }
  };


  return(
    <header
      className={`h-10 py-1 px-5 bg-primary flex items-center ${className}`}
    >
      <img
        src={ sidebarIcon }
        alt="sidebar"
        onClick={ () => { setShowSidebar(!showSidebar); } }
        className="h-75 mr-4 py-1 px-3 rounded-5 hover-bg-grey-25 cursor-pointer"
      />
      <h4 className="text-primary-dark">UnibenEngVault</h4>
      <ul>
        <li>{ user?.dept_code }</li>
        <li>{ user?.level_name}</li>
      </ul>

      <Button
        type="button"
        variant="secondary"
        size="md"
        onClick={ handleLogout }
        children="Logout"
        className="ml-auto"
      />
    </header>
  );
}
