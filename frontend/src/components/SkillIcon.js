import React from "react";

const SkillIcon = ({ skillName }) => {
  return (
    <div className="badge bg-light text-dark fw-normal mx-2 p-2 px-3 rounded shadow-sm">
      {skillName}
    </div>
  );
};

export default SkillIcon;
