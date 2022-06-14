import React, { useState, useEffect, createContext } from "react";

export const AuthContext = createContext();

const AuthContextProvider = (props) => {
  const [userToken, setUserToken] = useState(null);

  const storeTokenInfo = (userInfo) => {
    setUserToken(userInfo);
    console.log("stored in info start", userInfo);
    localStorage.setItem("userToken", JSON.stringify(userInfo));
  };

  const deleteTokenInfo = () => {
    localStorage.removeItem("userToken");
  };

  const getTokenInfo = () => {
    const userInfo = localStorage.getItem("userToken");

    return JSON.parse(userInfo);
  };
  
  return (
    <AuthContext.Provider value={{ storeTokenInfo, getTokenInfo, deleteTokenInfo }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
