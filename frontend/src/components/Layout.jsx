import Header from "./Header";
import Sidebar from "./Sidebar";

function Layout({ main }){
    return(
        <>
            <Header />
            <div>
                <Sidebar />
                {main}
            </div>
        </>
    );

}

export default Layout