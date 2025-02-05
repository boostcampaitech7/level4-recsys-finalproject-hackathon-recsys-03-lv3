import React from "react";
import "../style/SkillTag.css";

const getBackgroundColor = (score) => {
  // 점수에 따라 색상을 계산 (0 ~ 5 사이의 score)
  const percentage = Math.min(Math.max(score / 5, 0), 1); // 0 ~ 1로 정규화

  // 시작 색상 (#D9D9D9)와 끝 색상 (#17B294)을 RGB로 변환
  const startColor = { r: 255, g: 235, b: 107 }; //rgb(255, 235, 107)
  const endColor = { r: 23, g: 178, b: 148 }; // #17B294

  // 색상 계산 (비례식)
  const r = Math.round(startColor.r + (endColor.r - startColor.r) * percentage);
  const g = Math.round(startColor.g + (endColor.g - startColor.g) * percentage);
  const b = Math.round(startColor.b + (endColor.b - startColor.b) * percentage);

  return `rgb(${r}, ${g}, ${b})`;
};

const SkillIcon = ({ text, score }) => {
  return (
    <span
      style={{
        backgroundColor: getBackgroundColor(score),
      }}
      className="badge skill-badge"
    >
      {text} {score}
    </span>
  );
};

export default SkillIcon;
