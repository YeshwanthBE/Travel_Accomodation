import React, { useContext } from "react";
import "./Reviews.css";
import StarRating from "./StarRating";
import AuthContext from "./AuthContext";
export default function Reviews(props) {
  const { reviews } = props.reviews;
  const reviewItems = Array.isArray(reviews)
    ? reviews.map((review) => (
        <div key={review.reviewid} className="review">
          <div className="user-name">
            <h4>{review.userid}</h4>
          </div>
          <div className="rev">
            <p>{review.review}</p>
          </div>
          <div className="rating">
            <h4>{review.rating}&#128970;</h4>
          </div>
        </div>
      ))
    : null;
  const [starRating, setStarRating] = React.useState(0);
  const [mouseOverStar, setMouseOverStar] = React.useState(0);
  const [review, setReview] = React.useState("");
  function postReview() {
    const apiUrl = "";
    if (review.length === 0 || starRating === 0) {
      return;
    }
    const postData = {
      acmid: reviews.acmid,
      rating: starRating,
      review: review,
    };
    console.log(postData);
    fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
      })
      .then(() => {
        setStarRating(0);
        setReview("");
      })
      .catch((error) => {
        console.error("Error posting data:", error.message);
      });
  }
  return (
    <div className="reviews">
      <div className="review">
        <textarea
          name="userreview"
          id="myText"
          placeholder="Write your review!!"
          className="userrev"
          value={review}
          maxLength={500}
          onChange={(event) => setReview(event.target.value)}
        ></textarea>
        <div className="rating-submit">
          <div className="star-rating">
            {[1, 2, 3, 4, 5].map((index) => (
              <StarRating
                key={index}
                filled={index <= starRating || index <= mouseOverStar}
                onClick={() => setStarRating(index)}
                onMouseOver={() => setMouseOverStar(index)}
                onMouseLeave={() => setMouseOverStar(0)}
              />
            ))}
          </div>
          <button className="button" onClick={postReview}>
            Submit
          </button>
        </div>
      </div>
      {reviewItems}
    </div>
  );
}
