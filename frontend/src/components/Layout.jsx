import Header from "./Header";
import Sidebar from "./Sidebar";
import "./Layout.css"

function Layout({ main }){
    return(
        <>
            <Header />
            <div className="body-container">
                <Sidebar />
                {main}
            </div>
        </>
    );

}

export default Layout