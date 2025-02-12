import React from "react";
import "../style/StarRatings.css";

const MultiStarRating = ({ rating, numRates, totalStars = 5 }) => {
  const getStarClass = (index) => {
    if (rating > index + 0.5) return "star half";
    if (rating >= index + 1) return "star full";
    return "star empty";
  };

  return (
    <div className="star-rating-container">
      <div className="star-rating">
        {[...Array(totalStars)].map((_, index) => (
          <div key={index} className={getStarClass(index)}>
            ★
          </div>
        ))}
      </div>

      {/* 별점 점수 표시 */}
      <div className="score-display">{rating.toFixed(1)}</div>
      {numRates ? "(" + numRates + ")" : ""}
    </div>
  );
};

export default MultiStarRating;
