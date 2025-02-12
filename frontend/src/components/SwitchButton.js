import React, { useState, useEffect } from "react";
import "../style/SwitchButton.css";

function SwitchButton({ text, onChange, value }) {
  const [isActive, setIsActive] = useState(false);

  const handleToggle = () => {
    const newState = !isActive;
    setIsActive(newState);
    if (onChange) {
      onChange(newState);
    }
  };

  useEffect(() => {
    if (value !== undefined) {
      setIsActive(value);
    }
  }, [value]);

  return (
    <div className="switch-container">
      <input
        type="checkbox"
        className="switch-input"
        checked={isActive}
        onChange={handleToggle}
      />
      <div
        className={`switch ${isActive ? "active" : ""}`}
        onClick={handleToggle}
      >
        <div className="switch-toggle"></div>
      </div>
      <span className="switch-label">{text}</span>
    </div>
  );
}

export default SwitchButton;
