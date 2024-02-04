import React from "react";
import "./AccommodationDetails.css";
import PriceCalculator from "./PriceCalculator";
export default function AccommdationDetails(props) {
  const { accommodation } = props;
  return (
    <div className="description">
      <img
        src={accommodation.imgurl}
        alt="accommodation Image"
        className="imgsrc"
      />
      <div className="accommodation-details">
        <h3 className="title">{accommodation.name}</h3>
        <p className="acmdesc">{accommodation.description}</p>

        <div className="impdetails">
          <p>Location:{accommodation.location}</p>
          <p>{accommodation.rating}&#128970;</p>
          <p>Contact:{accommodation.phno}</p>
          <p>&#x20B9;{accommodation.price}/Day</p>
        </div>
      </div>
      <PriceCalculator
        accommodation={accommodation}
        bookings={props.bookings}
      />
    </div>
  );
}
