/**
 * 
 */

import { useState } from "react";

import { useAuth } from "../../pages/auth/AuthContext";
import Header from "./Header";
import { AdminSidebar, StudentSidebar } from "./Sidebar"

export default function AdminLayout({
  className,
  Page
}) {

  const [ showSidebar, setShowSidebar ] = useState(false);
  const { user } = useAuth();

  const Sidebar = user?.is_admin ? AdminSidebar : StudentSidebar

  return (
    <div
      className="flex flex-col gap-5"
    >

      <Header
        showSidebar={ showSidebar }
        setShowSidebar={ setShowSidebar }
        className={className}
      />
      
      <main
        className="flex gap-1"
      >
        {/* -------------------- SIDEBAR -------------------- */}
        <Sidebar
          showSidebar={showSidebar}
          className="w-18 max-w-20 ml-3 pl-5"
       />
        
        {/* -------------------- MAIN SECTION -------------------- */}
        <div
          className="w-75 mx-8"
        >
          { Page }
        </div>
      </main>
    </div>
  );
}
