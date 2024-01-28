import React from "react";
import filtericon from "../assets/filter.png";
import searchicon from "../assets/searchicon.png";
import "./SearchBar.css";

export default function SearchBar(props) {
  function handleSearchOptions(event) {
    const { name, value } = event.target;
    props.setSearchOptions((oldOptions) => ({
      ...oldOptions,
      [name]: value,
    }));
  }
  return (
    <div className="search-div">
      <div className="search-bar">
        <div className="filter">
          <input type="radio" id="priceip" name="sort" value="price" />
          <label htmlFor="priceip">Price &#8593;</label>

          <input type="radio" id="pricedn" name="sort" value="price desc" />
          <label htmlFor="pricedn">Price &#8595;</label>

          <input type="radio" id="rating" name="sort" value="rating desc" />
          <label htmlFor="rating">Rating &#8595;</label>
        </div>
        <img src={filtericon} className="filtericon"></img>
        <input
          type="text"
          name="name"
          placeholder="Name"
          onChange={handleSearchOptions}
        ></input>
        <input
          type="text"
          name="location"
          placeholder="Location"
          onChange={handleSearchOptions}
        ></input>
        <input
          type="date"
          name="checkin"
          placeholder="Checkin..."
          onChange={handleSearchOptions}
        ></input>
        <input
          type="date"
          name="checkout"
          placeholder="Checkout..."
          onChange={handleSearchOptions}
        ></input>
        <button className="searchbutton" onClick={props.getData}>
          <img src={searchicon} className="searchicon"></img>
        </button>
      </div>
    </div>
  );
}
