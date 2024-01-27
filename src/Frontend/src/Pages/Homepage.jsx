import React from "react";
import PageHeader from "../Components/PageHeader.jsx";
import SearchBar from "../Components/SearchBar.jsx";
import AccomodationList from "../Components/AccomodationList.jsx";
import "./homepage.css";
export default function Homepage(props) {
  return (
    <>
      <PageHeader isLoggedIn={true} isAdmin={false} />
      <SearchBar />
      <AccomodationList />
    </>
  );
}
