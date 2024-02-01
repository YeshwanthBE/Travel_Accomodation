import React from "react";
import "./PriceCalculator.css";
export default function PriceCalculator(props) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const [minCheckinDate, setMinCheckinDate] = React.useState();
  const [maxCheckinDate, setMaxCheckinDate] = React.useState();
  const [minCheckoutDate, setMinCheckoutDate] = React.useState();
  const [maxCheckoutDate, setMaxCheckoutDate] = React.useState();
  const { Accommodation } = props;
  let Bookings;
  if (props.Bookings.length > 0) {
    Bookings = JSON.parse(props.Bookings);
  }
  function checkBlockedDates(currentCheckinDate) {
    if (Bookings) {
      Bookings.forEach((element) => {
        const checkinDate = new Date(element.checkin);
        const checkoutDate = new Date(element.checkout);
        if (
          currentCheckinDate > checkinDate &&
          currentCheckinDate < checkoutDate
        )
          return checkoutDate;
      });
    }
    return false;
  }
  React.useEffect(() => {
    if (Bookings) {
      let currentMinDate = new Date();
      currentMinDate.setDate(today.getDate() + 1);
      let flag;
      while (true) {
        flag = checkBlockedDates(currentMinDate);
        if (flag) currentMinDate.setDate(flag.getDate + 1);
        else break;
      }
      setMaxCheckinDate(currentMinDate);
    }
  }, [Bookings]);
  return (
    <>
      <div className="booking">
        <div className="txt_field">
          <label>Checkin</label>
          <input
            type="date"
            name="checkin"
            id="checkin"
            // min={minCheckinDate.toISOString().split("T")[0]}
            // max={maxCheckinDate.toISOString().split("T")[0]}
            // onChange={handleDateChange}
            required
          />
        </div>
        <div className="txt_field">
          <label>Checkout</label>
          <input
            type="date"
            name="checkout"
            id="checkout"
            // min={minCheckoutDate.toISOString().split("T")[0]}
            // max={maxCheckoutDate.toISOString().split("T")[0]}
            // onChange={handleDateChange}
            required
          />
        </div>
        <span className="bills">
          <div className="bill" id="bill">
            <script>pricePerNight="{Accommodation.price}"</script>
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
