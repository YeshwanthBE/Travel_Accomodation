import React from "react";
import "./AccomodationList.css";
export default function AccomodationList(props) {
  const [accomodationsElements, setAccomodationsElements] = React.useState([]);
  const accomodations = props.accomodations;
  function accomodationElementCreater() {
    if (Array.isArray(accomodations)) {
      const elements = accomodations.map((Accomodation, index) => {
        console.log(Accomodation);
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

            <div className="acmend">
              {Accomodation.rating && (
                <p>{Accomodation.rating.toFixed(1)}&#128970;</p>
              )}
              <button className="button">Book</button>
            </div>
          </div>
        );
      });
      setAccomodationsElements(elements);
    } else {
      setAccomodationsElements([]);
    }
  }
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
