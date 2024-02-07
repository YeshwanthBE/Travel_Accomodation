import React from "react";
import { Link, Outlet } from "react-router-dom";
import "./PageHeader.css";

export default function PageHeader(props) {
  const dashboard = <button className="button">Dashboard</button>;
  const loggedin = (
    <>
      <button className="button">Profile</button>
      <button className="button">Logout</button>
    </>
  );
  const login = (
    <>
      <button className="button">Login</button>
    </>
  );
  return (
    <>
      <header className="Header">
        <div>
          <Link to="/">
            <button className="Heading">OneyesExplora!!</button>
          </Link>
        </div>
        <div className="Profilebuttons">
          {props.isAdmin && dashboard}
          {props.isLoggedIn ? loggedin : login}
        </div>
      </header>
      <Outlet />
    </>
  );
}
