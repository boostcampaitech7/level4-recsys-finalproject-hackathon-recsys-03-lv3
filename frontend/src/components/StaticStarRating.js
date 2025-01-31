import React from "react";
import "../style/StarRating.css";

const StaticStarRating = ({ rating, numRates, totalStars = 5 }) => {
  // 별의 클래스를 반환하는 함수
  const getStarClass = (index) => {
    if (rating > index + 0.5) return "star half"; // 반별
    if (rating >= index + 1) return "star full"; // 완전한 별
    return "star empty"; // 빈 별
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

export default StaticStarRating;
