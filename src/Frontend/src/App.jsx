import React, { useContext } from "react";
import "./App.css";
import Home from "./Pages/Home.jsx";
import Booking from "./Pages/Booking.jsx";
import { Route, Routes } from "react-router-dom";
import PageHeader from "./Components/PageHeader.jsx";
import AuthContext from "./Components/AuthContext.jsx";
function App() {
  const { isLoggedIn } = useContext(AuthContext);
  return (
    <Routes>
      <Route path="/" element={<PageHeader />}>
        <Route index element={<Home />} />
        <Route path="/booking/:acmid" element={<Booking />} />
      </Route>
    </Routes>
  );
}

export default App;
