import React from "react";
import "./AccommodationDetails.css";
export default function AccommdationDetails(props) {
  const { Accommodation } = props;
  return (
    <>
      <div className="imgdesc">
        <img
          src={Accommodation.image}
          alt="Accommodation Image"
          className="imgsrc"
        />
        <div>
          <div className="namedesc">
            <h3>{Accommodation.name}</h3>
            <p>{Accommodation.description}</p>
          </div>
          <div className="impdetails">
            <p>Location:{Accommodation.location}</p>
            <p>{Accommodation.rating}&#128970;</p>
            <p>Contact:{Accommodation.phno}</p>
            <p>&#x20B9;{Accommodation.price}/Day</p>
          </div>
        </div>
      </div>
    </>
  );
}
