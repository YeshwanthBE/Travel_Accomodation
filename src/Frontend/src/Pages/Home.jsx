import React from "react";
import PageHeader from "../Components/PageHeader.jsx";
import SearchBar from "../Components/SearchBar.jsx";
import AccommodationList from "../Components/AccommodationList.jsx";
import "./Home.css";
export default function Home(props) {
  const [searchOptions, setSearchOptions] = React.useState({
    name: "",
    location: "",
    checkin: "",
    checkout: "",
    minp: "",
    maxp: "",
    sort: "",
  });
  const [Accommodations, setAccommodations] = React.useState([]);
  function getData() {
    let apiUrl = "http://127.0.0.1:8080/showacms";
    const params = new URLSearchParams();
    params.append("name", searchOptions.name);
    params.append("location", searchOptions.location);
    params.append("checkin", searchOptions.checkin);
    params.append("checkout", searchOptions.checkout);
    params.append("sort", searchOptions.sort);
    apiUrl = apiUrl + "?" + params.toString();
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setAccommodations(JSON.parse(data));
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  }
  React.useEffect(getData, []);
  return (
    <>
      <SearchBar setSearchOptions={setSearchOptions} getData={getData} />
      <AccommodationList
        searchOptions={searchOptions}
        Accommodations={Accommodations}
      />
    </>
  );
}
