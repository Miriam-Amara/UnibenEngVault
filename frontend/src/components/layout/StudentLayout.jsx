/**
 * 
 */

import { useState } from "react";

import { useAuth } from "../../pages/auth/AuthContext";
import Header from "./Header";
import { AdminSidebar, StudentSidebar } from "./Sidebar"

export default function StudentLayout({
  Page,
  showModal
}) {

  const [ showSidebar, setShowSidebar ] = useState(true);
  const overflowHidden = showModal ? "h-25 overflow-y-hidden" : ""

  const { user } = useAuth();

  const Sidebar = user?.is_admin ? AdminSidebar : StudentSidebar

  return (
    <div
      className="flex flex-col gap-5"
    >

      <Header
        showSidebar={ showSidebar }
        setShowSidebar={ setShowSidebar }
        className="sticky top-0"
      />
      
      <main
        className={ `${overflowHidden} flex gap-1` }
      >
        {/* -------------------- SIDEBAR -------------------- */}
        <Sidebar
          showSidebar={showSidebar}
          className="w-18 h-100 max-w-20 ml-3 pl-5 sidebar"
       />
        
        {/* -------------------- MAIN SECTION -------------------- */}
        <div
          className="flex-grow w-75 max-w-85 mx-auto layout"
        >
          { Page }
        </div>
      </main>
    </div>
  );
}