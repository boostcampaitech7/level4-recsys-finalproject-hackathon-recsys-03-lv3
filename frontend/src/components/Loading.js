import React from "react";
import "../style/Images.css";

const Loading = () => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p className="loading-text">로딩 중...</p>
    </div>
  );
};

export default Loading;
