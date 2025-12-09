/**
 * 
 */



import React, { createContext, useContext, useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

import { fetchUserApi } from "../../api/users";


const AuthContext = createContext();


export function AuthProvider({ children }) {
  const [ user, setUser ] = useState(null);
  const [ loading, setLoading ] = useState(true);

  const login = (userData) => {setUser(userData); setLoading(false);}
  const logout = () => setUser(null);

  const fetchMe = async () => {
    try {
      const userData = await fetchUserApi("me");
      
      setUser(userData);
      setLoading(false);

    } catch {
      setUser(null);
    }
  };

  useEffect(() => {fetchMe()},[]);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}


export const useAuth = () => useContext(AuthContext);


export function AdminRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return(
      <p>Loading...</p>
    );
  }
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!user.is_admin) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
}
