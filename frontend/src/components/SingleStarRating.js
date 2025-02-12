import React from "react";
import "../style/StarRatings.css";

const SingleStarRating = ({ score = 0, reviewCount = null }) => {
  return (
    <div className="score-container">
      <span className="star-icon">★</span>

      {/* 점수 표시 */}
      <span className="score-display">{score.toFixed(1)}</span>

      {/* 리뷰 개수 (있을 때만 표시) */}
      {reviewCount !== null && reviewCount !== undefined && (
        <span className="review-count">({reviewCount})</span>
      )}
    </div>
  );
};

export default SingleStarRating;
