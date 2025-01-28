import React, { useState } from "react";
import "../style/StarRating.css";

const StarRating = ({ totalStars = 5 }) => {
  const [rating, setRating] = useState(0); // 실제 고정된 별점
  const [hoverRating, setHoverRating] = useState(0); // 마우스 호버 시 별점

  const handleMouseMove = (event, index) => {
    const { left, width } = event.currentTarget.getBoundingClientRect();
    const hoverValue = index + (event.clientX - left) / width; // 반칸 단위 계산
    setHoverRating(Math.round(hoverValue * 2) / 2); // 0.5 단위로 반올림
  };

  const handleClick = (event, index) => {
    const { left, width } = event.currentTarget.getBoundingClientRect();
    const clickValue = index + (event.clientX - left) / width; // 클릭 위치 기반 값
    const finalValue = Math.round(clickValue * 2) / 2; // 0.5 단위로 반올림

    if (rating === finalValue) {
      setRating(0); // 동일한 값이면 초기화
    } else {
      setRating(finalValue); // 고정
    }
    setHoverRating(0); // 호버 초기화
  };

  const handleMouseLeave = () => {
    setHoverRating(0); // 마우스가 나가면 호버 초기화
  };

  const getStarClass = (index, isHover) => {
    const value = isHover ? hoverRating : rating; // 호버 중이면 호버, 아니면 고정값 사용
    if (value >= index + 1) return "star full";
    if (value > index) return "star half";
    return "star empty";
  };

  return (
    <div className="star-rating-container">
      <div className="star-rating" onMouseLeave={handleMouseLeave}>
        {[...Array(totalStars)].map((_, index) => (
          <div
            key={index}
            className={getStarClass(index, hoverRating > 0)}
            onMouseMove={(e) => handleMouseMove(e, index)}
            onClick={(e) => handleClick(e, index)} // 클릭 시 정확한 값 계산
          >
            ★
          </div>
        ))}
      </div>
      {/* 별점 점수 표시 */}
      <div className="score-display">
        {hoverRating > 0 ? hoverRating.toFixed(1) : rating.toFixed(1)}
      </div>
    </div>
  );
};

export default StarRating;
