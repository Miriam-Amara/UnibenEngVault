
function Sidebar(){
    return(
        <aside>
            <nav>
                <ul>
                    <li></li>
                    <li><a href="/dashboard">Dashboard</a></li>
                </ul>

                <ul>
                    <li></li>
                    <li>
                        Users
                        <ul>
                            <li><a href="/users">Manage Users</a></li>
                            <li><a href="/levels">Manage Levels</a></li>
                            <li><a href="/departments">Manage Departments</a></li>
                    </ul>
                    </li>
                </ul>

                <ul>
                    <li></li>
                    <li>
                        Content
                        <ul>
                            <li><a href="/courses">Manage Courses</a></li>
                            <li><a href="/files">Manage Files</a></li>
                    </ul>
                    </li>
                </ul>
            
                <ul>
                    <li></li>
                    <li>
                        Support
                        <ul>
                            <li><a href="/report">Report</a></li>
                            <li><a href="/help">Help</a></li>
                            <li><a href="/feedback">Feedback</a></li>
                    </ul>
                    </li>
                </ul>
            
                <ul>
                    <li></li>
                    <li><a href="/notifications">Notifications</a></li>
                </ul>
            
                <ul>
                    <li></li>
                    <li><a href="/profile">Profile</a></li>
                </ul>
            </nav>
        </aside>
    );
}

export default Sidebar