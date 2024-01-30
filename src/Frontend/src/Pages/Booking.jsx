import React from "react";
import PageHeader from "../Components/PageHeader";
import { useParams } from "react-router-dom";
import AccommdationDetails from "../Components/AccommodationDetails";
function getData(apiUrl, setfunction) {
  fetch(apiUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      setfunction(data);
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}
export default function Booking() {
  const { acmid } = useParams();
  const [Accommodation, setAccommodation] = React.useState([]);
  const [Reviews, setReviwes] = React.useState([]);
  const [Bookings, setBookings] = React.useState([]);
  React.useEffect(() => {
    getData(`http://127.0.0.1:8083/acm/mod/?acmid=${acmid}`, setAccommodation);
    getData(`http://127.0.0.1:8096/reviews/?acmid=${acmid}`, setReviwes);
    getData(`http://127.0.0.1:8085/allacmbks?acmid=${acmid}`, setBookings);
  }, []);
  return (
    <>
      <PageHeader isLoggedIn={true} isAdmin={false} />
      <AccommdationDetails Accommodation={Accommodation} />
    </>
  );
}
