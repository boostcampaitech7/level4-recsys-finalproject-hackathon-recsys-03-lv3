import React from "react";
import "../style/InfoCard.css";

const InfoCard = ({ children, className = "" }) => {
  return <div className={`info-card card ${className}`.trim()}>{children}</div>;
};

export default InfoCard;
