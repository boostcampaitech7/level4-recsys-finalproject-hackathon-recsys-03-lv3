import React from "react";
import "../style/SkillIcon.css";

const getBackgroundColor = (score) => {
  // 점수에 따라 색상 계산
  const intensityRed = Math.floor(220 - score * 39.4);
  const intensityGreen = Math.floor(220 - score * 8.4);
  const intensityBlue = Math.floor(220 - score * 14.4);

  return `rgb(${intensityRed}, ${intensityGreen}, ${intensityBlue})`;
};

const SkillIcon = ({ text, score }) => {
  return (
    <span
      style={{
        backgroundColor: getBackgroundColor(score),
      }}
      className="badge skill-badge"
    >
      {text}
    </span>
  );
};

export default SkillIcon;
