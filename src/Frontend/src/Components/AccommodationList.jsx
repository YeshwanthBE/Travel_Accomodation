import React from "react";
import { Link } from "react-router-dom";
import "./AccommodationList.css";
export default function AccommodationList(props) {
  const [AccommodationsElements, setAccommodationsElements] = React.useState(
    []
  );
  const Accommodations = props.Accommodations;
  function AccommodationElementCreater() {
    if (Array.isArray(Accommodations)) {
      const elements = Accommodations.map((Accommodation, index) => {
        return (
          <div key={Accommodation.id || index} className="acm">
            <div className="acmimg">
              <img
                src={Accommodation.image}
                alt="Accommodation Image"
                className="imgsrc"
              />
            </div>
            <div className="acminfo">
              <h3>{Accommodation.name}</h3>
              <p>{Accommodation.description}</p>
            </div>

            <div className="acmend">
              {Accommodation.rating && (
                <p>{Accommodation.rating.toFixed(1)}&#128970;</p>
              )}
              <Link to={`/booking/${Accommodation.acmid}`}>
                <button className="button">Book</button>
              </Link>
            </div>
          </div>
        );
      });
      setAccommodationsElements(elements);
    } else {
      setAccommodationsElements([]);
    }
  }
  React.useEffect(AccommodationElementCreater, [Accommodations]);
  return (
    <div className="acms">
      {AccommodationsElements.length > 0 ? (
        AccommodationsElements
      ) : (
        <p className="filteredout">All Accommodations Filtered Out!!</p>
      )}
    </div>
  );
}
