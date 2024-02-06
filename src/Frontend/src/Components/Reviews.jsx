import React from "react";
import "./Reviews.css";
import StarRating from "./StarRating";
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
  return (
    <div className="reviews">
      <div className="review">
        <textarea
          name="userreview"
          id="myText"
          placeholder="Write your review!!"
          className="userrev"
        ></textarea>
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
      </div>
      {reviewItems}
    </div>
  );
}
