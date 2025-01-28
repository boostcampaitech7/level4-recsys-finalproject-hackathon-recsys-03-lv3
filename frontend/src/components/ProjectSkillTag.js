import React from "react";
import "../style/SkillTag.css";
import "../style/colors.css";

const SkillIcon = ({ text }) => {
  return (
    <span
      className="badge skill-badge"
      style={{ backgroundColor: "var(--color-secondary)" }}
    >
      {text}
    </span>
  );
};

export default SkillIcon;
