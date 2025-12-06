/**
 * 
 */

import { Link } from "react-router-dom";

// import usersIcon from "../../assets/users_icon.png";
// import coursesIcon from "../../assets/book_closed_icon.png";
// import supportIcon from "../../assets/support_icon.png";
// import profileIcon from "../../assets/user_icon.png";
import { useState } from "react";



export function AdminSidebar({
  showSidebar,
  className
}) {
  
  const [ showUsers, setShowUsers ] = useState(false);
  const [ showCourses, setShowCourses ] = useState(false);
  const [ showSupports, setShowSupports ] = useState(false);

  return (
    <>
    {showSidebar &&
    <aside
      className={ `${className}` }
    >
      <ul
        className="flex flex-col gap-2"
      >

        {/* ------------------------- DASHBOARD ------------------------- */}
        <li><Link to={"/dashboard"}>Dashboard</Link></li>

        {/* ------------------------- USERS DROPDOWN ------------------------- */}
        <li
          onClick={() => { setShowUsers(!showUsers); }}
          className="cursor-pointer"
        >
          Users
          {showUsers &&
          <ul
            className="text-grey-dark mt-1 py-1 px-2 bg-primary-light rounded-10 flex flex-col gap-1"
          >
            <li><Link to={"/departments"} className="text-grey-dark">Departments</Link></li>
            <li><Link to={"/levels"} className="text-grey-dark">Levels</Link></li>
            <li><Link to={"/users"} className="text-grey-dark">Users</Link></li>
          </ul>}
        </li>

        {/* ------------------------- COURSES DROPDOWN ------------------------- */}
        <li
          onClick={() => { setShowCourses(!showCourses); }}
          className="cursor-pointer"
        >
          Courses
          {showCourses &&
          <ul
            className="text-grey-dark mt-1 py-1 px-2 bg-primary-light rounded-10 flex flex-col gap-1"
          >
            <li><Link to={"/courses"} className="text-grey-dark">Courses</Link></li>
            <li><Link to={"/files"} className="text-grey-dark">Files</Link></li>
          </ul>}
        </li>

        {/* ------------------------- SUPPORTS DROPDOWN ------------------------- */}
        <li
          onClick={() => { setShowSupports(!showSupports); }}
          className="cursor-pointer"
        >
          Supports
          {showSupports &&
          <ul
            className="mt-1 py-1 px-2 bg-primary-light rounded-10 flex flex-col gap-1"
          >
            <li><Link to={"/reports"} className="text-grey-dark">Report</Link></li>
            <li><Link to={"/helps"} className="text-grey-dark">Help</Link></li>
            <li><Link to={"/feedbacks"} className="text-grey-dark">Feedback</Link></li>
          </ul>}
        </li>

        {/* ------------------------- PROFILE ------------------------- */}
        <li><Link to={"/profile"}>Profile</Link></li>
      </ul>
    </aside>
    }
    </>
  );
}



export function StudentSidebar({
  showSidebar,
  className
}) {

  const [ showSupports, setShowSupports ] = useState(false);

  return (
    <>
    {showSidebar &&
    <aside
      className={ `${className}` }
    >
      <ul
        className="flex flex-col gap-2"
      >

        {/* ------------------------- COURSES ------------------------- */}
        <li><Link to={"/courses"}>Courses</Link></li>

        {/* ------------------------- SUPPORTS DROPDOWN ------------------------- */}
        <li
          onClick={() => { setShowSupports(!showSupports); }}
          className="cursor-pointer"
        >
          Supports
          {showSupports &&
          <ul
            className="mt-1 py-1 px-2 bg-primary-light rounded-10 flex flex-col gap-1"
          >
            <li><Link to={"/reports"} className="text-grey-dark">Report</Link></li>
            <li><Link to={"/helps"} className="text-grey-dark">Help</Link></li>
            <li><Link to={"/feedbacks"} className="text-grey-dark">Feedback</Link></li>
          </ul>}
        </li>

        {/* ------------------------- PROFILE ------------------------- */}
        <li><Link to={"/profile"}>Profile</Link></li>
      </ul>
    </aside>
    }
    </>
  );
}
