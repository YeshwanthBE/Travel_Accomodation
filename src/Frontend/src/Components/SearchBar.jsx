import React from "react";
import filtericon from "../assets/filter.png";
import searchicon from "../assets/searchicon.png";
import "./SearchBar.css";

export default function SearchBar(props) {
  const [filterVisible, setFilterVisible] = React.useState(false);
  function handleSearchOptions(event) {
    const { name, value } = event.target;
    props.setSearchOptions((oldOptions) => ({
      ...oldOptions,
      [name]: value,
    }));
  }
  function toggleFilter(flag = 1) {
    setFilterVisible((prevVisible) => (flag === 0 ? false : !prevVisible));
  }
  return (
    <div className="search-div">
      <div className="search-bar">
        <div className={`filter ${filterVisible ? "visible" : ""}`}>
          <input
            type="radio"
            id="priceip"
            name="sort"
            value="price"
            onChange={handleSearchOptions}
          />
          <label htmlFor="priceip">Price &#8593;</label>

          <input
            type="radio"
            id="pricedn"
            name="sort"
            value="price desc"
            onChange={handleSearchOptions}
          />
          <label htmlFor="pricedn">Price &#8595;</label>

          <input
            type="radio"
            id="rating"
            name="sort"
            value="rating desc"
            onChange={handleSearchOptions}
          />
          <label htmlFor="rating">Rating &#8595;</label>
        </div>
        <button onClick={toggleFilter} className="filterbutton">
          <img src={filtericon} className="filtericon"></img>
        </button>
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
        <button
          className="searchbutton"
          onClick={() => {
            toggleFilter(0);
            props.getData();
          }}
        >
          <img src={searchicon} className="searchicon"></img>
        </button>
      </div>
    </div>
  );
}
