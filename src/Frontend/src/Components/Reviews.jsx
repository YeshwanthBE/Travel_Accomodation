import React from "react";
import "./Reviews.css";
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

  return (
    <div className="reviews">
      <div className="review">
        <textarea
          name="userreview"
          id="myText"
          placeholder="Write your review!!"
          class="userrev"
        ></textarea>
        <div className="star-rating"></div>
      </div>
      {reviewItems}
    </div>
  );
}
