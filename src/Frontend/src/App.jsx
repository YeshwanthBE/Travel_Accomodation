import React from "react";
import "./App.css";
import Home from "./Pages/Home.jsx";
import Booking from "./Pages/Booking.jsx";
import { Route, Routes } from "react-router-dom";
function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/booking/:acmid" element={<Booking />} />
    </Routes>
  );
}

export default App;
