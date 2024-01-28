import React from "react";
import "./AccomodationList.css";
export default function AccomodationList(props) {
  const [accomodations, setAccommodations] = React.useState([]);
  const [accomodationsElements, setAccomodationsElements] = React.useState([]);
  function getData() {
    var apiUrl = "http://127.0.0.1:8080/showacms";
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
  function accomodationElementCreater() {
    if (Array.isArray(accomodations)) {
      const elements = accomodations.map((Accomodation, index) => {
        return (
          <div key={Accomodation.id || index} className="acm">
            <div className="acmimg">
              <img
                src={Accomodation.image}
                alt="Accommodation Image"
                className="imgsrc"
              />
            </div>
            <div className="acminfo">
              <h3>{Accomodation.name}</h3>
              <p>{Accomodation.description}</p>
            </div>
            {Accomodation.rating && (
              <div className="acmend">
                <p>{Accomodation.rating}&#128970;</p>
              </div>
            )}
          </div>
        );
      });
      setAccomodationsElements(elements);
    } else {
      setAccomodationsElements([]);
    }
  }

  React.useEffect(getData, []);
  React.useEffect(accomodationElementCreater, [accomodations]);
  return (
    <div className="acmbody">
      <div className="acms">
        {accomodationsElements.length > 0 ? (
          accomodationsElements
        ) : (
          <p className="filteredout">All Accommodations Filtered Out!!</p>
        )}
      </div>
    </div>
  );
}
