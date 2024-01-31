import React from "react";
import "./PriceCalculator.css";
export default function PriceCalculator(props) {
  const { Accommodation } = props;
  return (
    <>
      <div className="booking">
        <div className="txt_field">
          <label>Checkin</label>
          <input
            type="date"
            name="checkin"
            id="checkin"
            // min={min_date}
            // max={max_date}
            required
          />
        </div>
        <div className="txt_field">
          <label>Checkout</label>
          <input
            type="date"
            name="checkout"
            id="checkout"
            // min={min_date}
            // max={max_date}
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
