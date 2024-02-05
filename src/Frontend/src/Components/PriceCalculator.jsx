import React from "react";
import "./PriceCalculator.css";
export default function PriceCalculator(props) {
  const [minCheckinDate, setMinCheckinDate] = React.useState(new Date());
  const [maxCheckinDate, setMaxCheckinDate] = React.useState(new Date());
  const [minCheckoutDate, setMinCheckoutDate] = React.useState(new Date());
  const [maxCheckoutDate, setMaxCheckoutDate] = React.useState();
  const checkinDates = [];
  const { accommodation } = props;
  const [priceDetails, setPriceDetails] = React.useState({});
  let bookings;
  if (props.bookings.length > 0) {
    bookings = JSON.parse(props.bookings);
  }
  React.useEffect(() => {
    if (bookings) {
      bookings.forEach((element) => {
        checkinDates.push(new Date(element.checkin));
      });
    }
  }, [bookings]);
  React.useEffect(() => {
    let newMinCheckinDate = minCheckinDate;
    while (true) {
      let temp = checkBlockedDates(newMinCheckinDate);
      if (!temp) break;
      newMinCheckinDate.setDate(temp.getDate() + 1);
    }
    setMinCheckinDate(newMinCheckinDate);
  }, [bookings]);
  React.useEffect(() => {
    const newMaxCheckinDate = new Date();
    newMaxCheckinDate.setDate(minCheckinDate.getDate() + 365);
    setMaxCheckinDate(newMaxCheckinDate);
  }, [minCheckinDate.getTime()]);
  function checkBlockedDates(currentCheckinDate) {
    let foundCheckoutDate = null;
    if (bookings) {
      bookings.forEach((element) => {
        const checkinDate = new Date(element.checkin);
        const checkoutDate = new Date(element.checkout);
        if (
          currentCheckinDate >= checkinDate &&
          currentCheckinDate <= checkoutDate
        ) {
          foundCheckoutDate = checkoutDate;
          return;
        }
      });
    }
    return foundCheckoutDate;
  }
  function nearestCheckinDate(bookingDate) {
    return checkinDates.reduce((prevDate, currentDate) => {
      if (currentDate > bookingDate && (!prevDate || currentDate < prevDate)) {
        return currentDate;
      } else {
        return prevDate;
      }
    }, null);
  }
  function handleCheckinDateChange(event) {
    const currentCheckinDate = new Date(event.target.value);
    currentCheckinDate.setHours(0, 0, 0, 0);
    const newMinCheckoutDate = new Date(currentCheckinDate);
    newMinCheckoutDate.setDate(newMinCheckoutDate.getDate() + 2);
    newMinCheckoutDate.setHours(0, 0, 0, 0);
    console.log(newMinCheckoutDate);
    setMinCheckoutDate(newMinCheckoutDate);
    let newMaxCheckoutDate = nearestCheckinDate(currentCheckinDate);
    if (newMaxCheckoutDate) {
      newMaxCheckoutDate.setDate(newMaxCheckoutDate.getDate() - 1);
    } else {
      newMaxCheckoutDate = new Date(currentCheckinDate);
      newMaxCheckoutDate.setHours(0, 0, 0, 0);
      newMaxCheckoutDate.setDate(newMaxCheckoutDate.getDate() + 60);
    }
    console.log(newMaxCheckoutDate);
    setMaxCheckoutDate(newMaxCheckoutDate);
  }
  function calculatePrice() {
    const checkinDate = new Date(document.getElementById("checkin").value);
    const checkoutDate = new Date(document.getElementById("checkout").value);
    if (!isNaN(checkinDate.getTime()) && !isNaN(checkoutDate.getTime())) {
      const nights = Math.floor(
        (checkoutDate - checkinDate) / (1000 * 60 * 60 * 24)
      );
      const innPrice = nights * accommodation.price;
      const GST = 0.18 * innPrice;
      const totalPrice = innPrice + GST * 2;
      setPriceDetails({ innPrice: innPrice, GST: GST, totalPrice: totalPrice });
    }
  }

  return (
    <>
      <div className="booking">
        <div className="txt_field">
          <label>Checkin</label>
          <input
            type="date"
            name="checkin"
            id="checkin"
            min={minCheckinDate && minCheckinDate.toISOString().split("T")[0]}
            max={maxCheckinDate.toISOString().split("T")[0]}
            onChange={handleCheckinDateChange}
            required
          />
        </div>
        <div className="txt_field">
          <label>Checkout</label>
          <input
            type="date"
            name="checkout"
            id="checkout"
            min={minCheckoutDate && minCheckoutDate.toISOString().split("T")[0]}
            max={maxCheckoutDate && maxCheckoutDate.toISOString().split("T")[0]}
            onChange={calculatePrice}
            required
          />
        </div>
        <span className="bills">
          <div className="bill" id="bill">
            <span>
              <p>Price:</p>
              <p id="price">
                {priceDetails.innPrice && priceDetails.innPrice + "₹"}
              </p>
            </span>
            <span>
              <p>18% SGST:</p>
              <p id="SGST">{priceDetails.GST && priceDetails.GST + "₹"}</p>
            </span>
            <span>
              <p>18% CGST:</p>
              <p id="CGST">{priceDetails.GST && priceDetails.GST + "₹"}</p>
            </span>
            <span>
              <p>Total:</p>
              <p id="Totalprice">
                {priceDetails.totalPrice && priceDetails.totalPrice + "₹"}
              </p>
            </span>
          </div>
        </span>
        <div className="booking-button">
          <button className="button">Book</button>
        </div>
      </div>
    </>
  );
}
