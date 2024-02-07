import React, { createContext, useState, useEffect } from "react";
const AuthContext = createContext();
export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  useEffect(() => {
    const token = localStorage.getItem("jwtToken");
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);
  const login = (jwtToken) => {
    localStorage.setItem("jwtToken", jwtToken);
    setIsLoggedIn(true);
  };
  const logout = () => {
    localStorage.removeItem("jwtToken");
    setIsLoggedIn(false);
  };
  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
export default AuthContext;
