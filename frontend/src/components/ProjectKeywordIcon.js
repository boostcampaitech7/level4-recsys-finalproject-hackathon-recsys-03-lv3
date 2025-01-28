import React from "react";
import "../style/ProjectKeywordIcon.css";

const ProjectKeywordIcon = ({ text, color }) => {
  return (
    <span
      style={{
        backgroundColor: color,
      }}
      className="badge keyword-badge"
    >
      {text}
    </span>
  );
};

export default ProjectKeywordIcon;
