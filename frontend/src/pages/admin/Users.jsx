import axios from "axios";
import { useEffect, useState } from "react";
import Layout from "../../components/Layout.jsx"

function getUsers(){
    const [users, setUsers] = useState([]);

    useEffect(() => {
        axios.get("/api/v1/users")
        .then((response) => {
            console.log(response.data());
            setUsers(response.data());
        })
    }, []);

    <div className="users-flex">
        {users.map((user) => {
          return (
            <div key={user.id} className="user-container">
                <div>

                </div>
            </div>
          )  
        })}
    </div>
}

function Users(){
    return(
        <>
            <title>UnibenEngVault-Users</title>
            <Layout /> 
        </>
    );
}

export default Users
