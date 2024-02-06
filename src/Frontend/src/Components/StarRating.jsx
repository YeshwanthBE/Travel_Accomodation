import React from "react";
import "./StarRating.css";
export default function StarRating(props) {
  return (
    <span
      className={`star ${props.filled ? "filled" : ""}`}
      onClick={props.onClick}
      onMouseOver={props.onMouseOver}
      onMouseLeave={props.onMouseLeave}
    >
      ★
    </span>
  );
}
