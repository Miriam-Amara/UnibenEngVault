import "./sidebar.css"
import "../assets/content_icon.png"
import "../assets/profile_icon.png"
import "../assets/support_icon.png"


function Sidebar(){
    return(
        <aside className="sidebar-nav">
                <ul className="main-nav">
                    {/* <li></li> */}
                    <li><a href="/dashboard">Dashboard</a></li>
                </ul>

                <ul className="main-nav">
                    {/* <li></li> */}
                    <li>
                        Users
                        <ul className="inner-nav">
                            <li><a href="/users">Manage Users</a></li>
                            <li><a href="/levels">Manage Levels</a></li>
                            <li><a href="/departments">Manage Departments</a></li>
                    </ul>
                    </li>
                </ul>

                <ul className="main-nav">
                    {/* <li><img src="content_icon" alt="Content" className="nav-icon" /></li> */}
                    <li>
                        Content
                        <ul className="inner-nav">
                            <li><a href="/courses">Manage Courses</a></li>
                            <li><a href="/files">Manage Files</a></li>
                    </ul>
                    </li>
                </ul>
            
                <ul className="main-nav">
                    {/* <li><img src="support_icon" alt="Support" className="nav-icon" /></li> */}
                    <li>
                        Support
                        <ul className="inner-nav">
                            <li><a href="/report">Report</a></li>
                            <li><a href="/help">Help</a></li>
                            <li><a href="/feedback">Feedback</a></li>
                    </ul>
                    </li>
                </ul>
            
                <ul className="main-nav">
                    <li></li>
                    <li><a href="/notifications">Notifications</a></li>
                </ul>
            
                <ul className="main-nav">
                    {/* <li><img src="profile_icon" alt="Profile" className="nav-icon" /></li> */}
                    <li><a href="/profile">Profile</a></li>
                </ul>
        </aside>
    );
}

export default Sidebar