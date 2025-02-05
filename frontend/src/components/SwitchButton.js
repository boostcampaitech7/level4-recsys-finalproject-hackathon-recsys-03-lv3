import React, { useState, useEffect } from "react";
import "../style/SwitchButton.css"; // CSS 파일 가져오기

function SwitchButton({ text, onChange, value }) {
  const [isActive, setIsActive] = useState(false);

  const handleToggle = () => {
    const newState = !isActive;
    setIsActive(newState);
    if (onChange) {
      onChange(newState); // 상태 변경 시 부모에 알림
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
