import React from "react";
import "./PriceCalculator.css";
export default function PriceCalculator(props) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const [minCheckinDate, setMinCheckinDate] = React.useState(new Date());
  const maxCheckinDate = new Date();
  maxCheckinDate.setDate(today.getDate() + 365);
  const [minCheckoutDate, setMinCheckoutDate] = React.useState(new Date());
  const [maxCheckoutDate, setMaxCheckoutDate] = React.useState();
  const checkinDates = [];
  const { accommodation } = props;
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
  function checkBlockedDates(currentCheckinDate) {
    if (bookings) {
      bookings.forEach((element) => {
        const checkinDate = new Date(element.checkin);
        const checkoutDate = new Date(element.checkout);
        if (
          currentCheckinDate >= checkinDate &&
          currentCheckinDate <= checkoutDate
        )
          return checkoutDate;
      });
    }
    return false;
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
    const newMinCheckoutDate = new Date();
    newMinCheckoutDate.setDate(currentCheckinDate.getDate() + 1);
    setMinCheckoutDate(newMinCheckoutDate);
    const newMaxCheckoutDate = new Date();
    newMaxCheckoutDate.setDate(
      nearestCheckinDate(currentCheckinDate).getDate() - 1
    );
    setMaxCheckoutDate(newMaxCheckoutDate);
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
            // onChange={handleDateChange}
            required
          />
        </div>
        <span className="bills">
          <div className="bill" id="bill">
            <script>pricePerNight="{accommodation.price}"</script>
            <span>
              <p>Price:</p>
              <p id="price"></p>
            </span>
            <span>
              <p>18% SGST:</p>
              <p id="SGST"></p>
            </span>
            <span>
              <p>18% CGST:</p>
              <p id="CGST"></p>
            </span>
            <span>
              <p>Total:</p>
              <p id="Totalprice"></p>
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
