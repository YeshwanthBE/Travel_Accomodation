import React from "react";
import "./AccommodationDetails.css";
import PriceCalculator from "./PriceCalculator";
export default function AccommdationDetails(props) {
  const { Accommodation } = props;
  return (
    <div className="description">
      <img
        src={Accommodation.imgurl}
        alt="Accommodation Image"
        className="imgsrc"
      />
      <div className="accommodation-details">
        <h3 className="title">{Accommodation.name}</h3>
        <p className="acmdesc">{Accommodation.description}</p>

        <div className="impdetails">
          <p>Location:{Accommodation.location}</p>
          <p>{Accommodation.rating}&#128970;</p>
          <p>Contact:{Accommodation.phno}</p>
          <p>&#x20B9;{Accommodation.price}/Day</p>
        </div>
      </div>
      <PriceCalculator
        Accommodation={Accommodation}
        Bookings={props.Bookings}
      />
    </div>
  );
}
